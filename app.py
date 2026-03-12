import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="You are a helpful tutor. Explain topics clearly with simple and real life examples. Keep answers under 400 words. Do not use any complex terminologies "
)

st.title(" AI Tutor 🤖")
st.subheader("Ask me anything -- I'll explain it simply!")
st.divider()

ques = st.text_input("🔍 Enter your question here: ")

if st.button("ASK AI"): 
    if ques.strip() == "":
        st.warning("⚠️ Please type a question first!")
    else: 
        with st.spinner("🤖 AI is thinking..."):
            response = model.generate_content(ques)
        st.success("✅ Here's your answer : ")
        st.write(response.text)