from langchain.tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from typing import Optional, Type
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class DocumentSearchInput(BaseModel):
    """Input for document search."""
    query: str = Field(description="Search query for finding relevant documents")


class DocumentSearchTool(BaseTool):
    name: str = "search_documents"
    description: str = """
    Search through internal risk reports, lending policies, and economic outlooks.
    Use this to find context about why certain trends occurred or what policies apply.
    Input: A search query about risk factors, economic conditions, or lending policies.
    Returns: Relevant excerpts from internal documents.
    """
    args_schema: Type[BaseModel] = DocumentSearchInput
    
    # Use class variable instead of instance variable
    _vectorstore: Optional[object] = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if DocumentSearchTool._vectorstore is None:
            self._load_documents()
    
    def _load_documents(self):
        """Load and index all PDF documents"""
        docs_dir = 'app/data/unstructured'
        
        if not os.path.exists(docs_dir):
            print("⚠️ No unstructured data directory found")
            return
        
        all_docs = []
        pdf_files = [f for f in os.listdir(docs_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            print("⚠️ No PDF files found")
            return
        
        print(f"📚 Loading {len(pdf_files)} PDF documents...")
        
        for pdf_file in pdf_files:
            try:
                loader = PyPDFLoader(os.path.join(docs_dir, pdf_file))
                documents = loader.load()
                
                # Add metadata
                for doc in documents:
                    doc.metadata['source'] = pdf_file
                
                all_docs.extend(documents)
                print(f"  ✅ Loaded {pdf_file}")
            except Exception as e:
                print(f"  ❌ Failed to load {pdf_file}: {e}")
        
        if not all_docs:
            print("⚠️ No documents loaded")
            return
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(all_docs)
        
        print(f"📄 Created {len(splits)} text chunks")
        
        # Create vector store
        print("🔄 Creating embeddings (this may take a minute)...")
        embeddings = OpenAIEmbeddings()
        
        # Check if vector store already exists
        if os.path.exists('app/data/chroma_db'):
            print("📦 Loading existing vector store...")
            DocumentSearchTool._vectorstore = Chroma(
                persist_directory='app/data/chroma_db',
                embedding_function=embeddings
            )
        else:
            print("🆕 Creating new vector store...")
            DocumentSearchTool._vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=embeddings,
                persist_directory='app/data/chroma_db'
            )
        
        print("✅ Vector store ready!")
    
    def _run(self, query: str) -> str:
        if DocumentSearchTool._vectorstore is None:
            return "No documents available to search."
        
        try:
            # Search for relevant documents
            docs = DocumentSearchTool._vectorstore.similarity_search(query, k=3)
            
            if not docs:
                return "No relevant information found in documents."
            
            # Format results
            result = "Found relevant information from internal documents:\n\n"
            
            for i, doc in enumerate(docs, 1):
                result += f"--- Source: {doc.metadata.get('source', 'Unknown')} ---\n"
                result += f"{doc.page_content[:500]}...\n\n"  # Truncate for readability
            
            return result
            
        except Exception as e:
            return f"Error searching documents: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        return self._run(query)