from rag import RAGPipeline

rag = RAGPipeline()

result = rag.answer_question(
    "What are Large Language Models?"
)

print(result["answer"])