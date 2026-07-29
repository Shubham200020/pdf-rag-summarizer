from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from services.vector_service import VectorService
import config

class RAGService:
    """Conversational RAG retrieval service with page citations, real-world web data access, and zero-config synthesis."""
    
    @staticmethod
    def fetch_web_search_context(query: str) -> List[Dict[str, Any]]:
        """Fetch live real-world web search data using DuckDuckGo search API."""
        web_results = []
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                for res in results:
                    web_results.append({
                        "page": "🌐 Web Search",
                        "file": res.get("title", "Live Web Result"),
                        "snippet": res.get("body", "")[:200] + "...",
                        "url": res.get("href", "")
                    })
        except Exception as e:
            print(f"[RAGService] Web search exception: {e}")
        return web_results

    @staticmethod
    def query(document_id: str, question: str, api_key: str = None, model_name: str = None, enable_web_search: bool = False) -> Dict[str, Any]:
        key = api_key or config.OPENAI_API_KEY
        model = model_name or config.DEFAULT_MODEL
        
        vector_store = VectorService.get_collection(document_id, api_key=key)
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        
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
            
        web_context_str = ""
        if enable_web_search:
            web_sources = RAGService.fetch_web_search_context(question)
            if web_sources:
                sources.extend(web_sources)
                web_context_str = "\n\n🌐 LIVE REAL-WORLD WEB DATA:\n" + "\n".join([
                    f"- {ws['file']}: {ws['snippet']} (URL: {ws.get('url', '')})" for ws in web_sources
                ])

        if key and key != "your_openai_api_key_here":
            try:
                context_text = "\n\n".join([
                    f"[Page {d.metadata.get('page_label', 'N/A')}]: {d.page_content}" 
                    for d in docs
                ]) + web_context_str
                
                llm = ChatOpenAI(temperature=0.2, model=model, openai_api_key=key)
                
                prompt = ChatPromptTemplate.from_messages([
                    ("system", (
                        "You are an expert AI document assistant and career strategy consultant.\n"
                        "Synthesize clear, well-structured, professional answers using the retrieved PDF context and real-world web data.\n"
                        "Structure your output cleanly using markdown bullet points and bold section headers.\n\n"
                        "RETRIEVED CONTEXT:\n{context}\n"
                    )),
                    ("human", "{question}")
                ])
                
                rag_chain = prompt | llm | StrOutputParser()
                answer = rag_chain.invoke({"context": context_text, "question": question})
                return {"answer": answer, "sources": sources}
            except Exception as e:
                print(f"[RAGService] OpenAI error: {e}. Falling back to zero-config synthesis.")

        # Zero-Config Retrieval Extractive Synthesizer
        if docs or enable_web_search:
            # Combine content across chunks
            combined_chunks = [d.page_content.strip() for d in docs]
            all_text = "\n".join(combined_chunks)
            
            lines = [l.strip() for l in all_text.split("\n") if l.strip()]
            
            # Extract key sections (skills, projects, education)
            bullet_points = []
            for line in lines:
                if any(k in line.lower() for k in ["skill", "project", "framework", "java", "python", "react", "angular", "engineered", "developed", "experience", "education", "college"]):
                    if len(line) > 15 and line not in bullet_points:
                        bullet_points.append(f"• {line}")
            
            summary_points = "\n".join(bullet_points[:8]) if bullet_points else "\n".join([f"• {l}" for l in lines[:5]])
            
            answer = f"### 📊 Synthesized Document Insights\n\n{summary_points}"
            
            if web_context_str:
                answer += f"\n\n### 🌐 Real-World Web Knowledge:\n{web_context_str}"
        else:
            answer = "I could not find relevant information in the provided PDF document."
            
        return {
            "answer": answer,
            "sources": sources
        }
