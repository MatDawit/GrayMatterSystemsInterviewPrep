import streamlit as st
import speech_recognition as sr
from openai import OpenAI

# --- CONFIGURATION ---
# Note: This requires streamlit >= 1.40.0
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

def transcribe_audio(audio_file):
    """
    Takes the audio file from the web recorder and transcribes it 
    using Google Speech Recognition.
    """
    r = sr.Recognizer()
    try:
        # Use the audio file object directly
        with sr.AudioFile(audio_file) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Error: Could not understand audio."
    except sr.RequestError:
        return "Error: Speech recognition API unavailable."
    except Exception as e:
        return f"Error processing audio: {e}"

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
    st.info("💡 **Web Mode:** You can now type your answer OR use the built-in recorder below the text box.")
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
    ], key="q1_select")
    
    st.markdown(f"**Question:** *{q1}*")
    
    # Text Input
    ans1 = st.text_area("Type your answer here:", height=100, key="text1")
    
    # Audio Input (Web Native)
    audio1 = st.audio_input("Or record your answer:", key="audio1")
    
    # Process Audio if present
    final_answer_1 = ans1
    if audio1:
        st.info("Processing audio...")
        transcribed_text = transcribe_audio(audio1)
        if "Error" not in transcribed_text:
            st.success(f"Transcribed: {transcribed_text}")
            final_answer_1 = transcribed_text
        else:
            st.error(transcribed_text)

    if st.button("Analyze Answer", key="btn1"):
        if final_answer_1:
            with st.spinner("Coach is analyzing..."):
                st.markdown(get_ai_feedback(api_key, "Recruiter Screen", q1, final_answer_1))
        else:
            st.warning("Please type or record an answer first.")

# === TAB 2: BEHAVIORAL (STAR) ===
with tab2:
    st.subheader("Behavioral Scenarios (STAR Method)")
    st.caption("Situation -> Task -> Action -> Result")
    
    q2 = st.selectbox("Select a Scenario:", [
        "Give me an example of a time when you had to deal with a difficult co-worker or fellow student on a project. How did you handle the situation? What were the outcomes?",
        "Tell me about a time when you had to persuade someone to see your point of view. What tactics did you use? What were the outcomes? What did you learn?",
        "Tell me about a time when you had a list of things to do and your supervisor/instructor came to you and said “I need this project/assignment completed by 5 o’clock”. How did you handle the situation?",
        "Tell me about a time you were involved in a project with a group.",
        "Give me an example of a time when you had to supervise someone.",
        "Tell me about how you keep yourself organized so to meet deadlines or goals.",
        "Give me an example of a time where you failed to meet a goal. What did you fail to do? What were the consequences? What was the outcome?",
        "Give me an example of a time when you used creativity to complete a project, work with someone else, or develop a new idea.",
        "Describe a time when you were a team leader. Who did the team consist of, and what did you do to help your team be successful?",
        "Describe a time when you were assigned a task but were provided little direction for how to complete the task. What steps did you take to complete the task? What was the outcome?",
        "Describe a time when a co-worker or student approached you and criticized your work. How did you handle the situation? What was the outcome?",
        "Provide me with an example of a time when you had to motivate others. What were the outcomes?",
        "Tell me about a time when you had to make a difficult decision that affected those with whom you worked. What was the outcome?"
    ], key="q2_select")
    
    st.markdown(f"**Question:** *{q2}*")
    
    ans2 = st.text_area("Type your STAR answer:", height=150, key="text2")
    audio2 = st.audio_input("Or record your answer:", key="audio2")
    
    final_answer_2 = ans2
    if audio2:
        st.info("Processing audio...")
        transcribed_text = transcribe_audio(audio2)
        if "Error" not in transcribed_text:
            st.success(f"Transcribed: {transcribed_text}")
            final_answer_2 = transcribed_text
        else:
            st.error(transcribed_text)

    if st.button("Analyze STAR Format", key="btn2"):
        if final_answer_2:
            with st.spinner("Checking your STAR structure..."):
                st.markdown(get_ai_feedback(api_key, "Behavioral STAR", q2, final_answer_2))
        else:
            st.warning("Please type or record an answer first.")

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
    ], key="q3_select")
    
    st.markdown(f"**Question:** *{q3}*")
    
    ans3 = st.text_area("Type your logic/explanation:", height=150, key="text3")
    audio3 = st.audio_input("Or record your answer:", key="audio3")
    
    final_answer_3 = ans3
    if audio3:
        st.info("Processing audio...")
        transcribed_text = transcribe_audio(audio3)
        if "Error" not in transcribed_text:
            st.success(f"Transcribed: {transcribed_text}")
            final_answer_3 = transcribed_text
        else:
            st.error(transcribed_text)

    if st.button("Analyze Logic", key="btn3"):
        if final_answer_3:
            with st.spinner("Analyzing technical accuracy..."):
                st.markdown(get_ai_feedback(api_key, "Technical", q3, final_answer_3))
        else:
            st.warning("Please type or record an answer first.")

# --- FOOTER ---
st.markdown("---")
st.caption("Powered by Streamlit & OpenRouter. This version is web-ready!")