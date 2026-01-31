import streamlit as st
import speech_recognition as sr
from openai import OpenAI
import threading

# --- CONFIGURATION ---
st.set_page_config(page_title="GrayMatter Interview Coach Pro", page_icon="🏭", layout="wide")

# --- CONTEXT & PROMPTS ---
JOB_CONTEXT = """
COMPANY: GrayMatter Systems
ROLE: Engineer I (Development Program)
VALUES: Accountability, Integrity, Respect, Innovation, Teamwork.
PROGRAM DETAILS: 2-year structured mentorship, hands-on field work, industrial automation.
KEY TRAITS: 'Thinking and Doing', owning mistakes (Accountability), learning agility (Innovation).
"""

SYSTEM_PROMPT = f"""
You are an expert Interview Coach specializing in Industrial Technology roles.
The user is applying for the 'Engineer I' role at GrayMatter Systems.
CONTEXT: {JOB_CONTEXT}

YOUR TASK:
Analyze the candidate's answer and provide structured, actionable feedback.
Output your response in the following Markdown format:

### 🟢 What You Did Well
(Point out specific phrases or logic that aligned with the role/values)

### 🟡 Areas for Improvement
(Critique the structure, tone, or missing details. Did they use STAR? Did they sound unsure?)

### 💡 Suggested "Level-Up" Phrasing
(Rewrite a sentence or two of their answer to make it sound more professional, specific, or impactful. Give 2 variations: one 'Confident/Direct' and one 'Thoughtful/Collaborative')
"""

# --- FUNCTIONS ---

def recognize_speech():
    """Records audio from the default microphone and converts it to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.toast("🎤 Listening... Speak now!")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=30)
            st.toast("✅ Processing audio...")
            text = r.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return "Error: No speech detected."
        except sr.UnknownValueError:
            return "Error: Could not understand audio."
        except sr.RequestError:
            return "Error: API unavailable."
        except Exception as e:
            return f"Error: {e}"

def get_ai_feedback(api_key, stage, question, answer):
    """Sends prompt to OpenRouter/Gemini."""
    if not api_key:
        return "⚠️ Please enter your OpenRouter API Key in the sidebar."
    
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    
    try:
        completion = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"STAGE: {stage}\nQUESTION: {question}\nCANDIDATE ANSWER: {answer}"}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error connecting to AI: {e}"

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("OpenRouter API Key", type="password")
    st.info("💡 **Voice Mode:** Click 'Start Recording' in the main window to speak your answer like a real interview.")
    st.markdown("---")
    st.markdown("**Core Values Cheatsheet:**\n\n* **Accountability:** Own it.\n* **Integrity:** Do the right thing.\n* **Respect:** Valuing others.\n* **Innovation:** Learning new things.\n* **Teamwork:** Collaboration.")

# --- MAIN APP ---
st.title("🏭 GrayMatter Interview Coach Pro")
st.markdown("Select a stage, pick a hard question, and **speak** or type your answer for instant coaching.")

# TABS
tab1, tab2, tab3 = st.tabs(["📞 Recruiter Screen", "⭐ Behavioral (STAR)", "🧠 Technical & Logic"])

# === TAB 1: RECRUITER SCREEN ===
with tab1:
    st.subheader("The 'Fit' Check")
    q1 = st.selectbox("Select a Question:", [
        "Tell me about yourself and why you want to start your career in Industrial Automation?",
        "GrayMatter is big on 'Accountability'. What does that mean to you in a workplace?",
        "This program involves travel to water plants and factories. How do you handle non-office environments?",
        "Where do you see yourself in 5 years, and how does this program help you get there?",
        "Why should we hire you over a candidate with more direct experience?"
    ])
    
    st.markdown(f"**Question:** *{q1}*")
    
    # Input Area
    col_a, col_b = st.columns([4, 1])
    with col_a:
        ans1 = st.text_area("Your Answer:", key="text1", height=100)
    with col_b:
        st.write(" ") 
        st.write(" ")
        if st.button("🎤 Record", key="rec1"):
            text = recognize_speech()
            if "Error" not in text:
                st.session_state['text1'] = text
                st.rerun()
            else:
                st.error(text)

    if st.button("Analyze Answer", key="btn1"):
        if ans1:
            with st.spinner("Coach is analyzing..."):
                st.markdown(get_ai_feedback(api_key, "Recruiter Screen", q1, ans1))
        else:
            st.warning("Please provide an answer first.")

# === TAB 2: BEHAVIORAL (STAR) ===
with tab2:
    st.subheader("Behavioral Scenarios (STAR Method)")
    st.caption("Situation -> Task -> Action -> Result")
    
    q2 = st.selectbox("Select a Scenario:", [
        "Tell me about a time you made a mistake that affected a client or project. How did you fix it?",
        "Describe a time you had to deal with a difficult team member who wasn't pulling their weight.",
        "Tell me about a time you were given a task with very vague instructions. What did you do?",
        "Describe a situation where you had to learn a complex technical tool overnight.",
        "Tell me about a time you disagreed with a supervisor or professor. How did you handle it?"
    ])
    
    st.markdown(f"**Question:** *{q2}*")
    
    col_a, col_b = st.columns([4, 1])
    with col_a:
        ans2 = st.text_area("Your STAR Answer:", key="text2", height=150)
    with col_b:
        st.write(" ")
        st.write(" ")
        if st.button("🎤 Record", key="rec2"):
            text = recognize_speech()
            if "Error" not in text:
                st.session_state['text2'] = text
                st.rerun()
            else:
                st.error(text)

    if st.button("Analyze STAR Format", key="btn2"):
        if ans2:
            with st.spinner("Checking your STAR structure..."):
                st.markdown(get_ai_feedback(api_key, "Behavioral STAR", q2, ans2))
        else:
            st.warning("Please provide an answer first.")

# === TAB 3: TECHNICAL & LOGIC ===
with tab3:
    st.subheader("Technical Aptitude & Logic")
    st.caption("Focus on troubleshooting steps and logical thinking, not just syntax.")
    
    q3 = st.selectbox("Select a Technical Challenge:", [
        "A client says their dashboard is 'frozen' and not showing new data. Walk me through how you troubleshoot this.",
        "Explain the concept of an IP Address and a Port to someone who knows nothing about computers.",
        "We have a temperature sensor. Write simple pseudocode to sound an alarm if the temp rises too fast (rate of change).",
        "How would you design a database table to store historical data for a factory machine's energy usage?",
        "You are onsite and the documentation for a machine is missing. How do you proceed?"
    ])
    
    st.markdown(f"**Question:** *{q3}*")
    
    col_a, col_b = st.columns([4, 1])
    with col_a:
        ans3 = st.text_area("Your Logic/Explanation:", key="text3", height=150)
    with col_b:
        st.write(" ")
        st.write(" ")
        if st.button("🎤 Record", key="rec3"):
            text = recognize_speech()
            if "Error" not in text:
                st.session_state['text3'] = text
                st.rerun()
            else:
                st.error(text)

    if st.button("Analyze Logic", key="btn3"):
        if ans3:
            with st.spinner("Analyzing technical accuracy..."):
                st.markdown(get_ai_feedback(api_key, "Technical", q3, ans3))
        else:
            st.warning("Please provide an answer first.")

# --- FOOTER ---
st.markdown("---")
st.caption("Tip: Speak clearly into your mic. The AI analyzes your 'spoken' transcript to help you sound natural.")