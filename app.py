import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
import json
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-lite",
        system_instruction="""
        You are an expert tutor. When explaining topics: 
        1. Always think step by step
        2. Do not ever use complex terminologies
        3. Always respond in this exact JSON format, nothing else: 

        {
            "topic": "", 
            "simple_explanation": "",
            "steps":[], 
            "real_world_example": "", 
            "difficulty": "Easy/Medium/Hard"
        }
        """
)

st.set_page_config(
    page_title="AI Tutor",
    page_icon="🤖",
    layout="centered"
)

st.title(" AI Tutor 🤖")
st.subheader("Ask me anything -- I'll explain it simply!")
st.divider()

ques = st.text_input("🔍 Enter your topic or question here: ")

if st.button("ASK AI"): 
    if ques.strip() == "":
        st.warning("⚠️ Please type a question first!")
    else: 
        with st.spinner("🤖 AI is thinking..."):
            response = model.generate_content(ques)

        try: 
            raw = response.text.strip()
            raw = raw.replace("```json", "").replace("```", "").strip()
            data = json.loads(raw)
            st.divider() #display results

            col1, col2 = st.columns(2)
            with col1: 
                st.metric(label="Topic", value=data['topic'])
            with col2: 
                st.metric(label="Difficulty", value=data['difficulty'])
            st.divider()

            st.subheader("Simple Explanation")
            st.info(data['simple_explanation'])

            st.subheader("📋 Step by Step")
            for i, step in enumerate(data['steps'], 1):
                if isinstance(step, dict):
                    title = step.get('title', '')
                    description = step.get('description', '')

                    with st.expander(f"{i}. {title}"):
                        st.write(description)

                else:
                    clean_step = step.replace("\\n", "\n")
                    st.write(f"**{i}.** {clean_step}")

            st.subheader("Real World Example")
            st.success(data['real_world_example'])
        
        except Exception as e:
            if "ResourceExhausted" in str(e):
                st.error("⚠️ Daily API limit reached. Please try again after some time.")
            elif "NotFound" in str(e):
                st.error("⚠️ AI model not available.")
            else:
                st.error("⚠️ Something went wrong. Please try again.")