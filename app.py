from dotenv import load_dotenv
import streamlit as st
import json
import os
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="AI Tutor",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Tutor")
st.subheader("Ask me anything — I'll explain it simply!")
st.divider()

question = st.text_input("🔍 Enter your topic or question here:")

if st.button("Ask AI"):

    if question.strip() == "":
        st.warning("⚠️ Please type a question first!")

    else:
        with st.spinner("🤖 AI is thinking..."):

        
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert tutor. When explaining any topic:
                        1. Think step by step before answering. Do not use complex terminologies
                        2. Respond ONLY in this exact JSON format, nothing else:
                        {
                            "topic": "",
                            "simple_explanation": "",
                            "steps": [],
                            "real_world_example": "",
                            "difficulty": "Easy/Medium/Hard"
                        }"""
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

        response_text = chat_completion.choices[0].message.content

        try:
            raw = response_text.strip()
            raw = raw.replace("```json", "").replace("```", "").strip()
            data = json.loads(raw)

            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="📚 Topic", value=data['topic'])
            with col2:
                st.metric(label="⚡ Difficulty", value=data['difficulty'])

            st.divider()

            st.subheader("💡 Simple Explanation")
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

            st.subheader("🌍 Real World Example")
            st.success(data['real_world_example'])

        except Exception as e:
            st.subheader("🤖 AI says:")
            st.write(response_text)
