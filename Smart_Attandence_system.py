from flask import Flask, Response, render_template_string, request, jsonify
import cv2
import csv
import os
from datetime import datetime
import webbrowser

app = Flask(__name__)

# CSV फाइल सेटअप
CSV_FILE = 'attendance.csv'
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Roll Number', 'Name', 'Date', 'Time'])

# OpenCV Haar Cascade लोड करें
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
camera = cv2.VideoCapture(0)

# लाइव वीडियो फ्रेम जनरेटर
def generate_frames():
    while True:
        if not camera.isOpened():
            break
        success, frame = camera.read()
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Face Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# सिंगल-फाइल HTML और CSS (सुंदर मॉडर्न लुक)
HTML_PAGE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Smart Attendance System</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .container { background: #1e293b; padding: 25px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); width: 100%; max-width: 900px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) { .container { grid-template-columns: 1fr; } }
        h1 { grid-column: 1 / -1; text-align: center; color: #38bdf8; font-size: 24px; margin-bottom: 10px; }
        .video-box { border: 2px solid #334155; border-radius: 12px; overflow: hidden; background: #000; display: flex; align-items: center; justify-content: center; }
        .video-box img { width: 100%; height: auto; display: block; }
        .form-box { display: flex; flex-direction: column; justify-content: center; gap: 15px; }
        .input-group { display: flex; flex-direction: column; gap: 5px; }
        label { font-size: 14px; color: #94a3b8; }
        input { padding: 12px; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: #fff; font-size: 16px; outline: none; }
        input:focus { border-color: #38bdf8; }
        button { padding: 12px; border-radius: 8px; border: none; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.2s; }
        .btn-submit { background: #0284c7; color: white; }
        .btn-submit:hover { background: #0369a1; }
        .btn-close { background: #ef4444; color: white; margin-top: 10px; }
        .btn-close:hover { background: #dc2626; }
        #msg { padding: 10px; border-radius: 8px; font-size: 14px; text-align: center; display: none; }
        .success { background: #15803d; color: white; }
        .warning { background: #b45309; color: white; }
        .error { background: #b91c1c; color: white; }
    </style>
</head>
<body>

<div class="container">
    <h1>AI Smart Attendance System</h1>
    
    <div class="video-box">
        <img src="/video_feed" alt="Live Camera Feed">
    </div>

    <div class="form-box">
        <div id="msg"></div>
        <div class="input-group">
            <label for="roll">रोल नंबर (Roll Number):</label>
            <input type="text" id="roll" placeholder="उदा. 101">
        </div>
        <div class="input-group">
            <label for="name">छात्र का नाम (Student Name):</label>
            <input type="text" id="name" placeholder="उदा. Abhishek">
        </div>
        <button class="btn-submit" onclick="submitAttendance()">अटेंडेंस लगाएँ (Mark Attendance)</button>
        <button class="btn-close" onclick="closeSystem()">सिस्टम तुरंत बंद करें (Close System)</button>
    </div>
</div>

<script>
    function showMsg(text, type) {
        const msg = document.getElementById('msg');
        msg.innerText = text;
        msg.className = type;
        msg.style.display = 'block';
        setTimeout(() => { msg.style.display = 'none'; }, 4000);
    }

    function submitAttendance() {
        const roll = document.getElementById('roll').value;
        const name = document.getElementById('name').value;

        fetch('/mark_attendance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ roll_no: roll, name: name })
        })
        .then(res => res.json())
        .then(data => {
            showMsg(data.message, data.status);
            if(data.status === 'success') {
                document.getElementById('roll').value = '';
                document.getElementById('name').value = '';
            }
        });
    }

    function closeSystem() {
        if(confirm("क्या आप वाकई सिस्टम बंद करना चाहते हैं?")) {
            fetch('/close_system', { method: 'POST' })
            .then(() => {
                document.body.innerHTML = "<h2 style='color:white; text-align:center;'>सिस्टम बंद कर दिया गया है। आप यह विंडो बंद कर सकते हैं।</h2>";
                setTimeout(() => { window.close(); }, 1000);
            });
        }
    }
</script>

</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    roll_no = data.get('roll_no', '').strip()
    name = data.get('name', '').strip()

    if not roll_no or not name:
        return jsonify({'status': 'error', 'message': 'कृपया रोल नंबर और नाम दोनों भरें!'})

    today_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    # डुप्लीकेट अटेंडेंस चेक (एक दिन में एक ही बार)
    already_marked = False
    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) >= 3 and row[0] == roll_no and row[2] == today_date:
                already_marked = True
                break

    if already_marked:
        return jsonify({'status': 'warning', 'message': f'रोल नंबर {roll_no} की अटेंडेंस आज पहले से दर्ज है!'})

    # CSV में सेव करें
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([roll_no, name, today_date, current_time])

    return jsonify({'status': 'success', 'message': f'अटेंडेंस दर्ज हुई: {name} ({roll_no})'})

@app.route('/close_system', methods=['POST'])
def close_system():
    global camera
    if camera.isOpened():
        camera.release()
    cv2.destroyAllWindows()
    # बैकग्राउंड में सर्वर और पाइथन प्रोसेस तुरंत बंद करने के लिए
    import threading
    threading.Timer(0.5, lambda: os._exit(0)).start()
    return jsonify({'status': 'closed'})

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5001')
    app.run(port=5001, debug=False)