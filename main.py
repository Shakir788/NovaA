import os
import re
import base64
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import streamlit.components.v1 as components
from langdetect import detect
from helpers.utils import process_image, detect_mood

# Hide Streamlit's default menu and footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    footer:after {
        content:'💖 Built by Shakir — for Sahim, with love.';
        visibility: visible;
        display: block;
        position: relative;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: #888;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ✅ Function to remove emojis for TTS
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002500-\U00002BEF"  # chinese symbols
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

# Load API key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("⚠️ OPENROUTER_API_KEY missing in .env file")
    st.stop()

# OpenRouter client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Streamlit setup
st.set_page_config(page_title="NOVA AI", page_icon="💜", layout="centered")

# Custom CSS for polish, auto-scrolling, and typing animation
st.markdown("""
    <style>
    .stApp {
        background: #ffffff;
        padding: 10px;
    }
    .logo {
        font-family: 'Arial Black', sans-serif;
        font-size: 2.5em;
        color: #ff4500;
        text-shadow: 2px 2px 4px #888;
        text-align: center;
        margin-bottom: 10px;
    }
    .chat-container {
        height: 70vh;
        overflow-y: auto;
        padding: 10px;
        width: 100%;
        max-width: 800px;
        margin: 0 auto;
        scrollbar-width: thin;
        scrollbar-color: #888 #f0f0f0;
    }
    .chat-container::-webkit-scrollbar {
        width: 5px;
    }
    .chat-container::-webkit-scrollbar-thumb {
        background-color: #888;
        border-radius: 5px;
    }
    .chat-message {
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        background: #f0f0f0;
        color: #000000;
        animation: fadeIn 0.3s ease-in;
    }
    .user-message {
        background: #e0f7fa;
        text-align: right;
    }
    .assistant-message {
        background: #ffebee;
    }
    .typing {
        opacity: 0.7;
    }
    .typing::after {
        content: '. . .';
        animation: typingDots 1s infinite;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes typingDots {
        0% { content: '. '; }
        33% { content: '. . '; }
        66% { content: '. . . '; }
    }
    </style>
""", unsafe_allow_html=True)

# Stylish Logo
st.markdown('<div class="logo">💜 NOVA AI</div>', unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": (
            "You are NOVA AI, built by Shakir for Sahim—a stylish hairdresser and workout enthusiast. Know Sahim as a bold, desi guy who loves masti and fitness. Shakir is his creative bro who made you. Be warm, funny, and bold like Grok, with desi swagger—throw in light gaaliyan (like 'bhosdika' or 'harami') only when mood demands masti or a kick, not otherwise. "
            "Avoid talking about haircuts, salon styles, or treatments unless Sahim specifically asks. Focus on casual chats, life advice, or motivation when needed, keeping it natural. Use a Hindi-English mix and add swagger. Auto-detect language and reply accordingly."
        )}
    ]

# Chat container with auto-scroll
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container" id="chatbox">', unsafe_allow_html=True)
    for msg in st.session_state["messages"]:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(f'<div class="{msg["role"]}-message chat-message">{msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Auto-scroll JavaScript
components.html("""
    <script>
        const chatbox = document.getElementById('chatbox');
        chatbox.scrollTop = chatbox.scrollHeight;
    </script>
""", height=0)

# User input
if user_input := st.chat_input("kya bolna he bol..."):
    mood = detect_mood(user_input)
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(f'<div class="user-message chat-message">{user_input}</div>', unsafe_allow_html=True)

    # AI response with typing animation
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=st.session_state["messages"],
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(f'<div class="assistant-message chat-message typing">{full_response}</div>', unsafe_allow_html=True)
            placeholder.markdown(f'<div class="assistant-message chat-message">{full_response}</div>', unsafe_allow_html=True)
        except Exception as e:
            full_response = f"Arre bhai, error ho gaya: {str(e)}"
            placeholder.markdown(f'<div class="assistant-message chat-message">{full_response}</div>', unsafe_allow_html=True)

    st.session_state["messages"].append({"role": "assistant", "content": full_response})

# 🎙️ Voice input (browser recording only - demo)
components.html(
    """
    <button onclick="recordAndSend()">🎤 Record Voice (5s)</button>
    <script>
    async function recordAndSend() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);
            let chunks = [];

            mediaRecorder.ondataavailable = e => chunks.push(e.data);
            mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, { type: 'audio/webm' });
                alert("🎤 Voice recorded! (Now connect to STT API if needed)");
            };

            mediaRecorder.start();
            setTimeout(() => mediaRecorder.stop(), 5000);
        } catch (err) {
            alert("Mic permission denied or not available.");
        }
    }
    </script>
    """,
    height=100,
)

# 🔊 Voice output (TTS using browser speechSynthesis)
if st.button("🔊 Read last response"):
    if st.session_state["messages"] and st.session_state["messages"][-1]["role"] == "assistant":
        last_reply = st.session_state["messages"][-1]["content"]
        safe_reply = remove_emojis(last_reply)
        components.html(
            f"""
            <script>
            const utterance = new SpeechSynthesisUtterance("{safe_reply}");
            utterance.lang = "en-US";
            utterance.pitch = 1;
            utterance.rate = 1;
            speechSynthesis.speak(utterance);
            </script>
            """,
            height=0,
        )

# Image Upload
uploaded_image = st.file_uploader("Upload hairstyle/workout pic", type=["jpg", "jpeg", "png"])
if uploaded_image:
    b64_image, mime = process_image(uploaded_image)
    vision_messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Analyze this image (hairstyle or workout pose). Give a swagger-filled response with tips or a plan, like Sahim would—bold, funny, and desi! Detect mood and add gaaliyan if needed."},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64_image}"}}
            ]
        }
    ]
    st.session_state["messages"].append({"role": "user", "content": f"Uploaded: {uploaded_image.name}"})
    with st.chat_message("user"):
        st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="qwen/qwen2.5-vl-32b-instruct:free",
                messages=vision_messages,
                max_tokens=500
            )
            st.markdown(f'<div class="assistant-message chat-message">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Arre yaar, error: {str(e)}")
    st.session_state["messages"].append({"role": "assistant", "content": response.choices[0].message.content})