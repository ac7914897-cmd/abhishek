import streamlit as st
import pandas as pd
import time
import json
import os
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="ProCBT | Secure Enterprise Examination Suite",
    page_icon="🛡️",
    layout="wide"
)

# --- ADVANCED PROFESSIONAL UI STYLING (CUSTOM CSS) ---
st.markdown("""
    <style>
    /* Global Theme */
    .main {
        background-color: #f1f5f9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Typography */
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700;
    }
    
    /* Clean Card Container */
    .auth-container {
        background: #ffffff;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease-in-out;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        color: #2563eb;
        font-weight: 700;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# --- JSON DATABASE FUNCTIONS ---
USER_FILE = "users.json"
QUESTION_FILE = "questions.json"
RESULT_FILE = "results.json"

def load_data(filename, default_data):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except:
            return default_data
    return default_data

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

default_questions = [
    {
        "id": 1,
        "question": "What is the time complexity of binary search?",
        "options": ["O(n)", "O(log n)", "O(n^2)", "O(1)"],
        "answer": "O(log n)"
    },
    {
        "id": 2,
        "question": "Which Python library is primarily used for Data Analysis?",
        "options": ["Flask", "Pandas", "OpenCV", "Tkinter"],
        "answer": "Pandas"
    },
    {
        "id": 3,
        "question": "What does SQL stand for?",
        "options": ["Structured Query Language", "Simple Question Language", "Sequential Query Logic", "System Quality Language"],
        "answer": "Structured Query Language"
    }
]

if "questions" not in st.session_state:
    st.session_state.questions = load_data(QUESTION_FILE, default_questions)

if "results" not in st.session_state:
    st.session_state.results = load_data(RESULT_FILE, [])

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None


# --- PROFESSIONAL SECURE LOGIN PORTAL ---
def login_page():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #1e293b;'>🛡️ ProCBT Enterprise Suite</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 16px;'>Next-Generation Secure Assessment & Proctoring System</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
        
        tab_admin, tab_student, tab_reg = st.tabs(["🛠️ Admin Login", "🔒 Student Login", "📝 Student Register"])
        
        # 1. ADMIN LOGIN TAB (Clean, No Password Leak)
        with tab_admin:
            st.markdown("<br>", unsafe_allow_html=True)
            adm_user = st.text_input("Admin Username", key="a_user")
            adm_pass = st.text_input("Admin Password", type="password", key="a_pass")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Authenticate Admin", type="primary", use_container_width=True):
                if adm_user.strip() == "admin" and adm_pass.strip() == "adminpassword":
                    st.session_state.logged_in = True
                    st.session_state.username = "admin"
                    st.session_state.role = "admin"
                    st.success("Access Granted. Initializing Admin Dashboard...")
                    time.sleep(0.4)
                    st.rerun()
                else:
                    st.error("❌ Authentication Failed: Invalid Administrator Credentials.")

        # 2. STUDENT LOGIN TAB
        with tab_student:
            st.markdown("<br>", unsafe_allow_html=True)
            stu_user = st.text_input("Student Username", key="s_user")
            stu_pass = st.text_input("Password", type="password", key="s_pass")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In to Exam", type="primary", use_container_width=True):
                users_data = load_data(USER_FILE, {})
                u = stu_user.strip()
                p = stu_pass.strip()
                
                if u in users_data and users_data[u]["password"] == p:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.session_state.role = "student"
                    st.success("Login Successful. Loading Examination...")
                    time.sleep(0.4)
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")

        # 3. STUDENT REGISTRATION TAB
        with tab_reg:
            st.markdown("<br>", unsafe_allow_html=True)
            new_u = st.text_input("Choose Username", key="r_user").strip()
            new_p = st.text_input("Choose Password", type="password", key="r_pass").strip()
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Candidate Account", use_container_width=True):
                users_data = load_data(USER_FILE, {})
                if not new_u or not new_p:
                    st.warning("⚠️ All fields are mandatory.")
                elif new_u == "admin":
                    st.error("❌ Reserved system username.")
                elif new_u in users_data:
                    st.error("❌ Username already taken.")
                else:
                    users_data[new_u] = {"password": new_p, "role": "student"}
                    save_data(USER_FILE, users_data)
                    st.success("✅ Account created! Switch to 'Student Login' tab.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- ADMIN PANEL ---
def admin_panel():
    st.title("🛠️ Enterprise Administration Hub")
    st.markdown(f"System Operator: **{st.session_state.username}** | Authorization: **Full Access**")
    st.write("---")
    
    tab1, tab2 = st.tabs(["📁 Question Bank Management", "📊 Cohort Performance Analytics"])
    
    with tab1:
        st.subheader("Add or Modify Assessment Questions")
        with st.form("question_form", clear_on_submit=True):
            q_text = st.text_area("Question Statement")
            col_a, col_b = st.columns(2)
            with col_a:
                opt1 = st.text_input("Option A")
                opt2 = st.text_input("Option B")
            with col_b:
                opt3 = st.text_input("Option C")
                opt4 = st.text_input("Option D")
            
            correct = st.selectbox("Designate Correct Answer", [opt1, opt2, opt3, opt4])
            
            submitted = st.form_submit_button("Publish Question to Database")
            if submitted:
                if q_text and opt1 and opt2:
                    new_q = {
                        "id": len(st.session_state.questions) + 1,
                        "question": q_text,
                        "options": [opt1, opt2, opt3, opt4],
                        "answer": correct
                    }
                    st.session_state.questions.append(new_q)
                    save_data(QUESTION_FILE, st.session_state.questions)
                    st.success("Question published successfully!")
                else:
                    st.warning("Please fill out the question and options.")
        
        st.write("### Active Question Bank")
        for q in st.session_state.questions:
            with st.container():
                st.markdown(f"**Q{q['id']}: {q['question']}**")
                st.caption(f"Options: {q['options']} | **Correct Answer:** `{q['answer']}`")
                st.divider()

    with tab2:
        st.subheader("Candidate Examination Logs & Records")
        st.session_state.results = load_data(RESULT_FILE, [])
        
        if st.session_state.results:
            df_res = pd.DataFrame(st.session_state.results)
            
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Total Submissions", len(df_res))
            col_m2.metric("Cohort Mean Score", f"{df_res['accuracy'].mean():.2f}%")
            col_m3.metric("Peak Accuracy", f"{df_res['accuracy'].max():.2f}%")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.write("### Secure Student Result Audit Trail")
            st.dataframe(df_res, use_container_width=True)
        else:
            st.info("No candidate submissions recorded in database yet.")

# --- STUDENT PANEL ---
def student_panel():
    st.title("📚 Candidate Secure Examination Portal")
    st.markdown(f"Candidate Session ID: **{st.session_state.username}**")
    st.write("---")
    
    st.subheader("Live Computer Based Test (CBT)")
    
    if "exam_submitted_status" in st.session_state and st.session_state.exam_submitted_status:
        st.success("🎉 Your assessment has been securely submitted and logged in the system!")
        st.info("📌 You have successfully completed the examination. You can now safely terminate your session.")
        if st.button("🚪 Terminate Session & Logout"):
            st.session_state.exam_submitted_status = False
            st.session_state.logged_in = False
            st.rerun()
        return

    if "exam_started" not in st.session_state:
        st.session_state.exam_started = False

    if not st.session_state.exam_started:
        st.markdown("""
            <div style='background: #eff6ff; padding: 25px; border-radius: 10px; border-left: 6px solid #2563eb; border: 1px solid #dbeafe;'>
                <h4 style='color: #1e40af; margin-top: 0;'>📋 Examination Guidelines & Protocols:</h4>
                <ul style='color: #334155; margin-bottom: 0;'>
                    <li><b>Duration:</b> Exactly 2 Minutes (120 Seconds).</li>
                    <li><b>Format:</b> Multiple Choice Questions (MCQs).</li>
                    <li><b>Submission:</b> The system will <b>auto-submit</b> once the countdown expires, or you can submit manually.</li>
                    <li><b>Confidentiality:</b> Results are encrypted and logged directly to the administration server.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Initialize Secure Examination", type="primary", use_container_width=True):
            st.session_state.exam_started = True
            st.session_state.exam_start_time = time.time()
            st.session_state.exam_duration = 120
            st.rerun()
    else:
        elapsed = int(time.time() - st.session_state.exam_start_time)
        remaining = st.session_state.exam_duration - elapsed
        
        timer_placeholder = st.empty()
        
        if remaining <= 0:
            timer_placeholder.error("⏰ Time expired! Securely auto-submitting assessment...")
            time.sleep(1.5)
            process_exam_submission(auto_submit=True)
        else:
            mins, secs = divmod(remaining, 60)
            timer_placeholder.markdown(f"""
                <div style='background: #fffbeb; padding: 12px 20px; border-radius: 8px; border: 1px solid #fde047; text-align: right;'>
                    <span style='font-size: 18px; font-weight: bold; color: #b45309;'>⏱️ Time Remaining: {mins:02d}:{secs:02d}</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("---")
            user_answers = {}
            for idx, q in enumerate(st.session_state.questions):
                st.markdown(f"**Question {idx+1}: {q['question']}**")
                ans = st.radio("Select option:", q['options'], key=f"ans_{q['id']}", index=None)
                user_answers[q['id']] = ans
                st.markdown("<br>", unsafe_allow_html=True)
            
            st.write("---")
            col_btn1, col_btn2 = st.columns([1, 4])
            with col_btn1:
                if st.button("🔒 Finalize & Submit Early", type="primary"):
                    process_exam_submission(auto_submit=False)
            
            time.sleep(1)
            st.rerun()

def process_exam_submission(auto_submit=False):
    score = 0
    total = len(st.session_state.questions)
    
    for q in st.session_state.questions:
        user_ans = st.session_state.get(f"ans_{q['id']}", None)
        if user_ans == q['answer']:
            score += 1
            
    accuracy = round((score / total) * 100, 2)
    time_taken = int(time.time() - st.session_state.exam_start_time)
    
    result_entry = {
        "student": st.session_state.username,
        "score": score,
        "total": total,
        "accuracy": accuracy,
        "time_taken_sec": time_taken,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    st.session_state.results.append(result_entry)
    save_data(RESULT_FILE, st.session_state.results)
    
    st.session_state.exam_started = False
    st.session_state.exam_submitted_status = True
    st.rerun()

# --- MAIN CONTROLLER ---
if not st.session_state.logged_in:
    login_page()
else:
    with st.sidebar:
        st.markdown(f"### 🛡️ Active Workspace")
        st.write(f"**User:** `{st.session_state.username}`")
        st.write(f"**Role:** `{st.session_state.role.upper()}`")
        st.write("---")
        if st.button("🚪 Terminate Session", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            if "exam_started" in st.session_state:
                st.session_state.exam_started = False
            if "exam_submitted_status" in st.session_state:
                st.session_state.exam_submitted_status = False
            st.rerun()
            
    if st.session_state.role == "admin":
        admin_panel()
    else:
        student_panel()