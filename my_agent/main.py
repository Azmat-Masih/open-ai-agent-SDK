import os
import google.generativeai as genai
from dotenv import load_dotenv
import nest_asyncio

# Allow nested async loops (needed if using Jupyter or event loops)
nest_asyncio.apply()

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

# Configure Gemini
genai.configure(api_key=api_key)

# Pick model
model = genai.GenerativeModel("gemini-1.5-flash")

# Example Agent-like function
def math_agent(question: str):
    prompt = f"You are a math tutor agent. Explain step by step: {question}"
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    question = "Why is learning math important for AI agents?"
    answer = math_agent(question)
    print("🤖 Agent Response:\n")
    print(answer)
