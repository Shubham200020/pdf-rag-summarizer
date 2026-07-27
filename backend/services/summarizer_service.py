from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
import config

class SummarizerService:
    """PDF Map-Reduce summarizer and roadmap generator service with fallback."""
    
    @staticmethod
    def generate_summary(chunks: List[Document], api_key: str = None, model_name: str = None) -> str:
        key = api_key or config.OPENAI_API_KEY
        model = model_name or config.DEFAULT_MODEL
        
        if key and key != "your_openai_api_key_here":
            try:
                llm = ChatOpenAI(temperature=0.2, model=model, openai_api_key=key)
                
                map_prompt = ChatPromptTemplate.from_messages([
                    ("system", "Summarize the key points of the following document section concisely:"),
                    ("human", "{text}")
                ])
                map_chain = map_prompt | llm | StrOutputParser()
                
                chunk_summaries = []
                for chunk in chunks[:15]:
                    summary = map_chain.invoke({"text": chunk.page_content})
                    chunk_summaries.append(summary)
                    
                combined_summaries = "\n\n".join(chunk_summaries)
                
                reduce_prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are an expert AI educator and technical analyst."),
                    ("human", (
                        "Based on the following document section summaries:\n\n"
                        "{text}\n\n"
                        "Generate a clear, beautifully structured report formatted in Markdown with two main sections:\n\n"
                        "### EXECUTIVE SUMMARY\n"
                        "Provide a high-level summary of the document, core objectives, and major takeaways.\n\n"
                        "### STEP-BY-STEP ROADMAP & ACTION PLAN\n"
                        "Create a chronological, phased learning or implementation roadmap based on the document contents."
                    ))
                ])
                reduce_chain = reduce_prompt | llm | StrOutputParser()
                return reduce_chain.invoke({"text": combined_summaries})
            except Exception as e:
                print(f"[SummarizerService] OpenAI error: {e}. Using extractive fallback.")

        # Zero-Config Extractive Summary Fallback
        doc_text_snippets = [c.page_content[:250].strip() for c in chunks[:6]]
        summary_bullets = "\n".join([f"- {s}..." for s in doc_text_snippets])
        
        roadmap_phases = "\n".join([
            f"1. **Phase {i+1} (Section {i+1})**: {chunk.page_content[:120].strip()}..."
            for i, chunk in enumerate(chunks[:5])
        ])
        
        return f"""### EXECUTIVE SUMMARY (Extractive Fallback)
The document contains {len(chunks)} text chunks across key topics. Key sections include:

{summary_bullets}

---

### STEP-BY-STEP ROADMAP & ACTION PLAN
{roadmap_phases}

> Note: Paste a valid OpenAI API key in the top bar to unlock full LLM synthesis.
"""
