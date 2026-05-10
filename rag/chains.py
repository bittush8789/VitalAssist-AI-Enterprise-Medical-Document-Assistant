from rag.vector_store import vector_db_manager
from llm.groq_client import groq_client
from llm.prompts import RAG_PROMPT

class RAGChain:
    def __init__(self):
        self.manager = vector_db_manager

    def answer_question(self, question: str):
        # 1. Retrieve relevant chunks (more chunks = fuller answers)
        retriever = self.manager.get_retriever(k=5)
        docs = retriever.invoke(question)
        
        # 2. Extract context
        context = "\n---\n".join([doc.page_content for doc in docs])
        
        if not context.strip():
            return "I could not find information in the uploaded medical report.", []

        # 3. Build Prompt (strict, detailed)
        prompt = f"""
You are an expert medical AI assistant. Answer the question using ONLY the provided medical context.
Give a COMPLETE and DETAILED answer. Include ALL relevant information found in the context such as:
- Patient details (name, age, ID)
- Doctor/physician names
- Diagnosis and conditions
- Medications and dosages
- Lab results with values
- Procedures performed
- Insurance information
- Dates and timelines

Do NOT truncate or summarize. Provide the FULL information.
If the answer is not found in the context, say:
"I could not find information in the uploaded medical report."

Context:
{context}

Question:
{question}

Provide a complete, detailed answer:
"""
        
        # 4. Generate Answer
        answer = groq_client.get_completion(prompt, system_message="You are an expert medical AI.")
        
        return answer, docs

rag_chain = RAGChain()
