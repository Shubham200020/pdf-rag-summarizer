from typing import Dict, Any, List
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from services.vector_service import VectorService
import config

class RAGService:
    """Conversational RAG retrieval service with page citations, real-world web data access, and smart query-aware zero-config synthesis."""
    
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
                
                # Temperature set strictly to 0.0 for zero hallucination and exact grounding
                llm = ChatOpenAI(temperature=0.0, model=model, openai_api_key=key)
                
                prompt = ChatPromptTemplate.from_messages([
                    ("system", (
                        "You are an expert AI document assistant and career strategy consultant.\n"
                        "Synthesize clear, strictly grounded, accurate answers using the retrieved PDF context and real-world web data.\n"
                        "Maintain zero hallucination. Structure your output cleanly using markdown bullet points and bold section headers.\n\n"
                        "RETRIEVED CONTEXT:\n{context}\n"
                    )),
                    ("human", "{question}")
                ])
                
                rag_chain = prompt | llm | StrOutputParser()
                answer = rag_chain.invoke({"context": context_text, "question": question})
                return {"answer": answer, "sources": sources}
            except Exception as e:
                print(f"[RAGService] OpenAI error: {e}. Falling back to smart query-aware synthesis.")

        # Smart Query-Aware Extractive Synthesizer (Zero-Config Mode)
        if docs or enable_web_search:
            # Tokenize question into relevant keywords
            stopwords = {"what", "is", "the", "are", "about", "his", "her", "my", "me", "give", "tell", "more", "a", "an", "and", "or", "in", "on", "for", "with", "to", "of"}
            q_words = [w.lower() for w in re.findall(r'\w+', question) if w.lower() not in stopwords]
            
            extracted_sentences = []
            for doc in docs:
                page_label = doc.metadata.get("page_label", doc.metadata.get("page", "1"))
                content = doc.page_content.strip()
                # Split content into logical sentences or bullet points
                lines = [l.strip() for l in re.split(r'[\n\.\•\-\|]', content) if len(l.strip()) > 15]
                
                for line in lines:
                    line_lower = line.lower()
                    # Calculate relevance score based on keyword matches
                    match_count = sum(1 for kw in q_words if kw in line_lower)
                    if match_count > 0 or not q_words:
                        extracted_sentences.append((match_count, page_label, line))

            # Sort sentences by relevance score descending
            extracted_sentences.sort(key=lambda x: x[0], reverse=True)
            
            seen = set()
            top_bullets = []
            for score, pg, text in extracted_sentences:
                if text.lower() not in seen:
                    seen.add(text.lower())
                    top_bullets.append(f"• **(Page {pg})**: {text}")
                if len(top_bullets) >= 6:
                    break

            if not top_bullets:
                # Fallback to top sentences from retrieved chunks
                for doc in docs[:3]:
                    pg = doc.metadata.get("page_label", "1")
                    clean_lines = [l.strip() for l in doc.page_content.split('\n') if len(l.strip()) > 15]
                    for l in clean_lines[:2]:
                        if l.lower() not in seen:
                            seen.add(l.lower())
                            top_bullets.append(f"• **(Page {pg})**: {l}")

            formatted_points = "\n".join(top_bullets) if top_bullets else "No specific matching details found."
            answer = f"### 📌 Relevant Information Found in Document\n\n{formatted_points}"
            
            if web_context_str:
                answer += f"\n\n### 🌐 Real-World Web Knowledge:\n{web_context_str}"
        else:
            answer = "I could not find relevant information in the provided PDF document."
            
        return {
            "answer": answer,
            "sources": sources
        }
