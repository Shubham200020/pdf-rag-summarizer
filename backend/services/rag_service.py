from typing import Dict, Any, List
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from services.vector_service import VectorService
import config

class RAGService:
    """Conversational RAG retrieval service with page citations, real-world web search, and section-targeted answer synthesis."""
    
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
        retriever = vector_store.as_retriever(search_kwargs={"k": 6})
        
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

        # If OpenAI API Key is available, use LLM synthesis
        if key and key != "your_openai_api_key_here":
            try:
                context_text = "\n\n".join([
                    f"[Page {d.metadata.get('page_label', 'N/A')}]: {d.page_content}" 
                    for d in docs
                ]) + web_context_str
                
                llm = ChatOpenAI(temperature=0.0, model=model, openai_api_key=key)
                
                prompt = ChatPromptTemplate.from_messages([
                    ("system", (
                        "You are an expert AI document assistant and career strategy consultant.\n"
                        "Synthesize clear, strictly grounded, accurate answers directly targeting the user's question.\n"
                        "Do NOT include contact details (phone, email, github) unless explicitly requested by the user.\n"
                        "Structure your output cleanly using markdown bullet points and bold section headers.\n\n"
                        "RETRIEVED CONTEXT:\n{context}\n"
                    )),
                    ("human", "{question}")
                ])
                
                rag_chain = prompt | llm | StrOutputParser()
                answer = rag_chain.invoke({"context": context_text, "question": question})
                return {"answer": answer, "sources": sources}
            except Exception as e:
                print(f"[RAGService] OpenAI error: {e}. Falling back to Section-Targeted Extractive Synthesizer.")

        # 🎯 Section-Targeted Extractive Synthesizer (Zero-Config Local Mode)
        q_lower = question.lower()
        
        # Topic Intent Classification
        is_skills_query = any(k in q_lower for k in ["skill", "skills", "language", "languages", "frontend", "backend", "database", "stack", "tech"])
        is_projects_query = any(k in q_lower for k in ["project", "projects", "apk", "product", "system", "app", "website", "freelance"])
        is_experience_query = any(k in q_lower for k in ["experience", "intern", "job", "work", "settribe", "tipco", "company"])
        is_education_query = any(k in q_lower for k in ["education", "college", "degree", "msc", "bsc", "cgpa", "marks"])
        is_contact_query = any(k in q_lower for k in ["contact", "phone", "mobile", "email", "github", "linkedin", "address"])
        
        extracted_bullets = []
        seen = set()
        
        for doc in docs:
            pg = doc.metadata.get("page_label", doc.metadata.get("page", "1"))
            content = doc.page_content
            lines = [l.strip() for l in re.split(r'[\n\•\-\➢]', content) if len(l.strip()) > 8]
            
            for line in lines:
                l_lower = line.lower()
                
                # Filter out contact info lines unless specifically requested
                if not is_contact_query and any(h in l_lower for h in ["mobile:", "email:", "github:", "linkedin:", "shubham kumar", "career objective"]):
                    continue
                    
                matched = False
                if is_skills_query and any(k in l_lower for k in ["technical skills", "languages:", "frontend:", "backend:", "databases:", "tools:", "concepts:", "java", "python", "angular", "react", "spring boot", "mysql", "postgresql", "mongodb", "aws", "git", "linux"]):
                    matched = True
                elif is_projects_query and any(k in l_lower for k in ["project", "apk elite", "product management", "engineered", "developed", "description:", "technology used:"]):
                    matched = True
                elif is_experience_query and any(k in l_lower for k in ["intern", "settribe", "tipco", "feb 2024", "june 2026", "developed and maintained"]):
                    matched = True
                elif is_education_query and any(k in l_lower for k in ["msc", "b.sc", "college", "cgpa", "senior secondary", "higher secondary"]):
                    matched = True
                elif not (is_skills_query or is_projects_query or is_experience_query or is_education_query):
                    matched = True

                if matched and line not in seen:
                    seen.add(line)
                    extracted_bullets.append(f"• **(Page {pg})**: {line}")

        if extracted_bullets:
            bullet_text = "\n".join(extracted_bullets[:7])
            heading_title = "Technical Skills" if is_skills_query else ("Projects" if is_projects_query else ("Experience" if is_experience_query else "Extracted Context"))
            answer = f"### 📌 {heading_title}\n\n{bullet_text}"
        else:
            # Fallback to top non-contact lines across chunks
            fallback_lines = []
            for doc in docs:
                pg = doc.metadata.get("page_label", "1")
                lines = [l.strip() for l in doc.page_content.split('\n') if len(l.strip()) > 12]
                for l in lines:
                    if not any(h in l.lower() for h in ["mobile:", "email:", "github:", "linkedin:", "shubham kumar"]):
                        if l not in seen:
                            seen.add(l)
                            fallback_lines.append(f"• **(Page {pg})**: {l}")
            answer = f"### 📌 Relevant PDF Context\n\n" + ("\n".join(fallback_lines[:5]) if fallback_lines else "I could not find relevant information in the provided PDF document.")

        if web_context_str:
            answer += f"\n\n### 🌐 Real-World Web Knowledge:\n{web_context_str}"
            
        return {
            "answer": answer,
            "sources": sources
        }
