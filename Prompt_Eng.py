import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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

print("🤖 Smart AI Tutor -  Now with Structured Output!")
print("=" *50)

while True:
    topic = input("\n🔍 Enter a topic to learn: ")

    if topic.lower() == "quit": 
        print("Goodbye! Keep learning! 👋")
        break

    response = model.generate_content(topic)

    try: 
        raw = response.text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)

        print("\n" + "=" * 50)
        print(f"Topic: {data['topic']}")
        print(f"Difficulty: {data['difficulty']}")
        print(f"\n Simple Explantion:\n{data['simple_explanation']}")
        print(f"\n Step by Step: ")
        for i, step in enumerate (data['steps'], 1):
            print(f"   {i}. {step}")
        print(f"\n Real World Example:\n{data['real_world_example']}")
        print("=" * 50)

    except:
        print("\n🤖 AI Says: ")
        print(response.text)  