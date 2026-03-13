import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-lite",
    system_instruction="You are a helpful tutor. Explain topics clearly with simple examples. Keep answers under 150 words. "
)

print("🤖 AI Tutor is Ready! Type 'quit' to exit.\n")

while True:
    topic = input("🔍 Ask me anything: ")

    if topic.lower() == "quit": 
        print("Goodbye! Keep learning! 👋")

    response = model.generate_content(topic)
    print("🤖 AI Says: ")
    print(response.text)
    print("-" * 50)