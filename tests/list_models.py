import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = genai.Client(api_key=os.getenv("OPENROUTER_API_KEY"))

for model in client.models.list():
    print(model.name)