from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStore
import config

class RAGEngine:
    """Conversational RAG Chain Engine supporting question answering with citations using LCEL."""
    
    def __init__(self, vector_store: VectorStore, api_key: str = None, model_name: str = None):
        self.vector_store = vector_store
        self.api_key = api_key or config.OPENAI_API_KEY
        self.model_name = model_name or config.DEFAULT_MODEL
        
        self.llm = ChatOpenAI(
            temperature=0.1,
            model=self.model_name,
            openai_api_key=self.api_key
        )
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        
    def query(self, question: str) -> Dict[str, Any]:
        docs = self.retriever.invoke(question)
        context_text = "\n\n".join([
            f"[Page {d.metadata.get('page_label', 'N/A')}]: {d.page_content}" 
            for d in docs
        ])
        
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
        
        chain = prompt | self.llm | StrOutputParser()
        answer = chain.invoke({"context": context_text, "question": question})
        
        sources = []
        for doc in docs:
            page = doc.metadata.get("page_label", doc.metadata.get("page", "Unknown"))
            file_name = doc.metadata.get("source_file", "PDF Document")
            snippet = doc.page_content[:150].replace("\n", " ") + "..."
            sources.append({
                "page": page,
                "file": file_name,
                "snippet": snippet
            })
            
        return {
            "answer": answer,
            "sources": sources
        }
