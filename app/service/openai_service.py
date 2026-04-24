import json
from openai import OpenAI
from app.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

async def generate_reply(messages):
  streem = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages,
    stream=True
  )

  for chunk in streem:
    if chunk.choices[0].delta.content:
      yield chunk.choices[0].delta.content


def get_ambedding(text: str):
  res = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
  )

  return res.data[0].embedding