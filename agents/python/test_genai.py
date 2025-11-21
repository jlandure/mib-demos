from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

response = client.models.generate_content(
   model="gemini-3-pro-preview",
   contents="What's Men in Black movie about?",
   config=types.GenerateContentConfig(
       thinking_config=types.ThinkingConfig(
           thinking_level=types.ThinkingLevel.LOW # For fast and low latency response
       )
   ),
)

print(response.text)

