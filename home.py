import streamlit as st
import pandas as pd
import hashlib
import json
import os
import streamlit.components.v1 as components
#  CSS Styling
st.markdown("""
    <style>
        .main {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding-top: 100px;
            font-family: 'Segoe UI', sans-serif;
        }
        .login-container {
            background-color: #f9f9f9;
            padding: 40px 30px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            width: 350px;
            margin: auto;
        }
        .login-title {
            text-align: center;
            font-size: 26px;
            margin-bottom: 25px;
            color: #333;
        }
        .stTextInput > div > div > input {
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #ccc;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 0;
            width: 100%;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("""
                    <div style='
                        background-color: #e8f5e9;
                        border-left: 7px solid #4CAF50;
                        border-radius: 10px;
                        padding: 20px;
                        font-family: "Segoe UI", sans-serif;
                        color: #333;
                        text-align: center;'>
                    <h1 style='color:#4CAF50;'>	🤖 Welcome to Data Vision Studio!</h2>
            <p style='font-size: 18px; margin-top: 10px;'>✨ Let's get started on your Data Analysis journey..</p>
        </div>
    </div>
                """, unsafe_allow_html=True)
# hide streamlit sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="collapsedControl"] {
        display: none;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

#  Features
st.markdown("""
<div style='
    background-color: #FFFFFF;
    border: 2px dashed #64B5F6;
    border-radius: 12px;
    padding: 20px;
    font-family: "Segoe UI", sans-serif;
    color: #1A237E;
    margin-top: 10px;
    <h3 style='color: #1565C0;'>🌟 Features</h3>
    <ul style='text-align: left; font-size: 16px; line-height: 1.8; padding-left: 20px;'>
        <li>✅ <b>Easy to use</b> – no technical skills required</li>
        <li>🤖 <b>Build and deploy ML models</b> without writing code</li>
        <li>📊 <b>Supports multiple visualizations</b> (bar, line, scatter, heatmaps, etc.)</li>
        <li>📁 <b>Upload CSV files</b> and get instant results</li>
        <li>🧠 <b>Interactive SQL Workspace</b> to query your data</li>
        <li>📝 <b>PDF Report Generation</b> for your charts like Power BI</li>
        <li>💬 <b>Collect feedback</b> from users for improvement</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Custom CSS for button styling
st.markdown("""
    <style>
    .like-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 18px;
        border: none;
        cursor: pointer;
    }
    .like-button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("👍 Yes, I like it"):
        options = st.selectbox("How Would You Rate Us?",
                ["⭐️⭐️⭐️⭐️⭐️ Excellent", "⭐️⭐️⭐️⭐️ Good", "⭐️⭐️⭐️ Average", "⭐️⭐️ Poor", "⭐ Bad"],
                key="rating_select")
        if options:
            # Show the feedback message instantly
            st.info(f"🎯 You rated us: {options}")

with col2:
    if st.button("👎 No, I didn't like it", key="dislike_btn"):
        feedback = st.text_input("Your Feedback:", placeholder="Enter Your Feedback Here...", key="dislike_name_input")

        if feedback:
            st.warning(f"Sorry to hear that, {feedback}. We appreciate your honesty!")
            options = st.selectbox("What went wrong?",
                ["👎 Too Slow", "👎 Confusing UI", "👎 Missing Features", "👎 Bugs/Errors", "👎 Other"],
                key="dislike_reason_select")
            
            if options:
                st.info(f"📝 You mentioned: {options}")
            
#  Password Hashing 
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#  Load & Save Users 
def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

# Session Setup
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""

users = load_users()
st.markdown("---")
st.title("🔐 Login or Sign Up")

# Authentication Form 
menu = st.selectbox("Choose an option", ["Login", "Sign Up"])

st.markdown("""
                    <div style='
                        background-color: #e8f5e9;
                        border-left: 7px solid #4CAF50;
                        border-radius: 10px;
                        padding: 20px;
                        font-family: "Segoe UI", sans-serif;
                        color: #333;
                        text-align: center;'>
                    <h1 style='color:#4CAF50;'>	🤖 Lets Login To Get Started!</h2>
            <p style='font-size: 18px; margin-top: 10px;'>🌟 Please enter your credentials below:</p>
        </div>
    </div>
                """, unsafe_allow_html=True)

username = st.text_input("Username")
password = st.text_input("Password", type="password")
action_btn = st.button(menu)

if action_btn:
    if menu == "Sign Up":
        if username in users:
            st.error("🚫 Username already exists!")
        else:
            users[username] = hash_password(password)
            save_users(users)
            st.success("✅ Account created! You can now log in.")
    elif menu == "Login":
        if username in users and users[username] == hash_password(password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"✅ Welcome, {username}!")
            st.switch_page("pages/dashboard.py")
        else:
            st.error("❌ Invalid username or password")

st.markdown("</div>", unsafe_allow_html=True)

#  Post-login Redirect
if st.session_state['logged_in']:
    st.success(f"Welcome back, {st.session_state['username']}!")
    st.page_link("pages/dashboard.py", label="👉 Go to Dashboard")