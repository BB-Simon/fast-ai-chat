from openai import OpenAI
from app.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

async def generate_reply(message: str):
  response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
      {"role": "user", "content": message}
    ]
  )

  return response.choices[0].message.content
