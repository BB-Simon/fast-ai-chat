import numpy as np
import json

from app.service.openai_service import get_ambedding


def cosine_similarity(a, b):
  return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_relevant_chunks(question, chunks, top_k=3):
  q_emb = get_ambedding(question)
  scored = []

  for chunk in chunks:
    emb = np.array(json.loads(chunk.embedding))
    score = cosine_similarity(q_emb, emb)
    scored.append((score, chunk.content))

  scored.sort(reverse=True)
  return [c for _, c in scored[:top_k]]


def build_prompt(user_question: str, document_text: str):
  return f"""
  Answer the question based on the document below.

  Document:
  {document_text[:3000]}

  Question:
  {user_question}
"""
