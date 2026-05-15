"""
Crown of Kaliyug — Groq LLM Client
Phase 1: Story Engine
"""
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
    
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment")
        
    return ChatGroq(
        api_key=api_key,
        model_name=model,
        temperature=0.7
    )

def call_groq(prompt: str, system: str = "You are a specialized writing agent for the Crown of Kaliyug epic series."):
    client = get_groq_client()
    messages = [
        ("system", system),
        ("human", prompt)
    ]
    response = client.invoke(messages)
    return response.content

if __name__ == "__main__":
    # Quick test
    try:
        print("Testing Groq Connectivity...")
        res = call_groq("Hello! Are you ready to write the Crown of Kaliyug?")
        print(f"Response: {res}")
    except Exception as e:
        print(f"Error: {e}")
