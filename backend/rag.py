import google.generativeai as genai

from config import GEMINI_API_KEY
from vector_store import VectorStore
from chat_memory import ChatMemory


genai.configure(api_key=GEMINI_API_KEY)
print("GEMINI_API_KEY FOUND:", bool(GEMINI_API_KEY))

class RAGPipeline:
    def __init__(self):
        self.vector_store = VectorStore()
        self.memory = ChatMemory()

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    def answer_question(self, question, filename=None):
        sources = self.vector_store.search(
        query=question,
        top_k=3,
        filename=filename
    )
        

        context = "\n\n".join(
            [
                f"Source: {source['filename']} | Chunk: {source['chunk_index']}\n{source['content']}"
                for source in sources
            ]
        )

        chat_history = "\n".join(
            [
                f"{msg['role'].upper()}: {msg['content']}"
                for msg in self.memory.get_history()[-6:]
            ]
        )

        
        prompt = f"""
You are an AI Business Operations Copilot.

Use ONLY the provided document context to answer the question.
Use chat history only to understand follow-up questions.

Selected Document:
{filename if filename else "All uploaded documents"}

Chat History:
{chat_history}

Document Context:
{context}

Current Question:
{question}

Rules:
- If the answer is not in the document context, say:
"I could not find this information in the uploaded documents."
- Do not invent facts.
- Keep the answer clear and business-focused.

Answer:
"""
        response = self.model.generate_content(prompt)

        answer = response.text

        self.memory.add_message("user", question)
        self.memory.add_message("assistant", answer)

        return {
            "answer": answer,
            "sources": sources
        }

    def clear_memory(self):
        self.memory.clear()