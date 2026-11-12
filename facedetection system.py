import cv2

# XML फाइल का पूरा और सही पाथ या लोकल फोल्डर से लोड करें
face_cap = cv2.CascadeClassifier(  'haarcascade_frontalface_default.xml')

# चेक करें कि फाइल लोड हुई या नहीं
if face_cap.empty():
    print("Error: Haar Cascade XML file not loaded properly!")
else:
    video_cap = cv2.VideoCapture(0)
    
    while True:
        ret, video_data = video_cap.read()
        if not ret:
            break
            
        col = cv2.cvtColor(video_data, cv2.COLOR_BGR2GRAY)
        faces = face_cap.detectMultiScale(
            col,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        for (x, y, w, h) in faces:
            cv2.rectangle(video_data, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
        cv2.imshow("Video_Live", video_data)
        
        if cv2.waitKey(10) == ord("a"):
            break
            
    video_cap.release()
    cv2.destroyAllWindows()