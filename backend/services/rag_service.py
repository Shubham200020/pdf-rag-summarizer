from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from services.vector_service import VectorService
import config

class RAGService:
    """Conversational RAG retrieval service with page citations and zero-config fallback."""
    
    @staticmethod
    def query(document_id: str, question: str, api_key: str = None, model_name: str = None) -> Dict[str, Any]:
        key = api_key or config.OPENAI_API_KEY
        model = model_name or config.DEFAULT_MODEL
        
        vector_store = VectorService.get_collection(document_id, api_key=key)
        retriever = vector_store.as_retriever(search_kwargs={"k": 4})
        
        docs = retriever.invoke(question)
        sources = []
        for doc in docs:
            page = doc.metadata.get("page_label", doc.metadata.get("page", "Unknown"))
            file_name = doc.metadata.get("source_file", "Document")
            snippet = doc.page_content[:180].replace("\n", " ") + "..."
            sources.append({
                "page": page,
                "file": file_name,
                "snippet": snippet
            })
            
        if key and key != "your_openai_api_key_here":
            try:
                context_text = "\n\n".join([
                    f"[Page {d.metadata.get('page_label', 'N/A')}]: {d.page_content}" 
                    for d in docs
                ])
                llm = ChatOpenAI(temperature=0.1, model=model, openai_api_key=key)
                
                prompt = ChatPromptTemplate.from_messages([
                    ("system", (
                        "You are an expert AI document assistant.\n"
                        "Use ONLY the following context retrieved from the user's PDF to answer the question:\n\n"
                        "{context}\n\n"
                        "If the answer is not present in the context, state clearly: "
                        "'I could not find relevant information in the provided PDF document.'"
                    )),
                    ("human", "{question}")
                ])
                
                rag_chain = prompt | llm | StrOutputParser()
                answer = rag_chain.invoke({"context": context_text, "question": question})
                return {"answer": answer, "sources": sources}
            except Exception as e:
                print(f"[RAGService] OpenAI error: {e}. Falling back to context snippet extraction.")

        # Zero-Config Retrieval Extractive Fallback
        if docs:
            top_excerpt = docs[0].page_content.strip()
            answer = f"Based on the retrieved context (Page {sources[0]['page']}):\n\n\"{top_excerpt}\""
        else:
            answer = "I could not find relevant information in the provided PDF document."
            
        return {
            "answer": answer,
            "sources": sources
        }
