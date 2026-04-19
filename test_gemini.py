import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Setup the client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_with_gemini(text):
    # System instructions ensure the AI focuses on sarcasm/slang
    system_prompt = (
        "You are a sentiment analyzer specialized in YouTube comments. "
        "Analyze the sentiment of the following text as POSITIVE, NEGATIVE, or NEUTRAL. "
        "Be highly sensitive to sarcasm and internet slang. "
        "Output ONLY the word: POSITIVE, NEGATIVE, or NEUTRAL."
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview", # Use the latest 2026 flash model
            config={'system_instruction': system_prompt},
            contents=text
        )
        return response.text.strip().upper()
    except Exception as e:
        return f"ERROR: {e}"

# --- TEST THE SARCASM AGAIN ---
test_sentences = [
    "Brilliant. This tutorial explained absolutely nothing.",
    "This beat is actually disgusting. I'm literally dead right now. 💀",
    "Oh wow, another 10-minute unskippable ad. Just what I wanted."
]

print("--- Gemini Sarcasm Test ---")
result = analyze_with_gemini(test_sentences[1])
print(f"Text: {test_sentences[1]}\nResult: {result}\n")