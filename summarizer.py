from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
import config

class PDFSummarizer:
    """Provides document summarization and learning roadmap generation using LCEL."""
    
    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or config.OPENAI_API_KEY
        self.model_name = model_name or config.DEFAULT_MODEL
        self.llm = ChatOpenAI(
            temperature=0.2,
            model=self.model_name,
            openai_api_key=self.api_key
        )
        
    def generate_summary_and_roadmap(self, chunks: List[Document]) -> str:
        map_prompt = ChatPromptTemplate.from_messages([
            ("system", "Summarize the key points of the following document section concisely:"),
            ("human", "{text}")
        ])
        map_chain = map_prompt | self.llm | StrOutputParser()
        
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
                "### 📌 EXECUTIVE SUMMARY\n"
                "Provide a high-level summary of the document, core objectives, and major takeaways.\n\n"
                "### 🗺️ STEP-BY-STEP ROADMAP & ACTION PLAN\n"
                "Create a chronological, phased learning or implementation roadmap based on the document contents."
            ))
        ])
        reduce_chain = reduce_prompt | self.llm | StrOutputParser()
        return reduce_chain.invoke({"text": combined_summaries})
