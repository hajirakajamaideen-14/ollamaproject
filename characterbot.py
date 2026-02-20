import streamlit as st
import requests
import random
import time

# ---------------- CONFIG ----------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3:8b"

st.set_page_config(page_title="Mr Bean AI", layout="wide")

# ---------------- SESSION MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "username" not in st.session_state:
    st.session_state.username = None

# ---------------- PREMIUM CSS ----------------
st.markdown("""
<style>
/* Animated Gradient Background */
body {
    background: linear-gradient(-45deg, #2C3E50, #4CA1AF, #3A6073, #16222A);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Glass Chat Box */
.chat-box {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 10px;
    color: white;
    font-size: 18px;
}

/* Teddy Rain */
.teddy {
    position: fixed;
    top: -50px;
    font-size: 40px;
    animation: fall linear infinite;
}
@keyframes fall {
    to { transform: translateY(110vh); }
}

/* Mini Car */
.car {
    position: fixed;
    bottom: 20px;
    left: -200px;
    font-size: 40px;
    animation: drive 5s linear;
}
@keyframes drive {
    to { left: 110%; }
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="title">🎭 Mr Bean AI – Interactive Comedy Experience</div>', unsafe_allow_html=True)

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    st.markdown(f'<div class="chat-box"><b>{msg["role"].capitalize()}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# ---------------- USER INPUT ----------------
user_input = st.chat_input("Talk to Mr Bean...")

def call_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "gemma3:1b",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

# ---------------- LOGIC ----------------
if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})

    # Detect name
    if "my name is" in user_input.lower():
        name = user_input.split("is")[-1].strip()
        st.session_state.username = name

    # Special Modes
    lower_input = user_input.lower()

    if "teddy" in lower_input:
        for i in range(15):
            left = random.randint(0, 100)
            duration = random.randint(3, 8)
            st.markdown(
                f'<div class="teddy" style="left:{left}%; animation-duration:{duration}s;">🧸</div>',
                unsafe_allow_html=True
            )

    if "car" in lower_input:
        st.markdown('<div class="car">🚗</div>', unsafe_allow_html=True)

    # Typing Animation
    with st.spinner("Mr Bean is thinking... 🤔"):

        base_prompt = f"""
        You are Mr Bean. 
        Be funny, expressive, dramatic and slightly silly.
        Keep responses short and entertaining.
        User name: {st.session_state.username}
        Conversation:
        {st.session_state.messages}
        """

        reply = call_ollama(base_prompt)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()