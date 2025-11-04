import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from app.agents.financial_analyst import FinancialAnalystAgent
from dotenv import load_dotenv
import time

load_dotenv()

# Page config
st.set_page_config(
    page_title="Financial Analyst Agent",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    with st.spinner("🔄 Initializing agent..."):
        st.session_state.agent = FinancialAnalystAgent()
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.session_state.total_duration = 0

if 'show_reasoning' not in st.session_state:
    st.session_state.show_reasoning = True

# Header
st.markdown('<p class="main-header">💼 Financial Data Analyst Agent</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered analysis of loan portfolio performance with multi-step reasoning</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 Example Queries")
    st.markdown("Click any example to try it:")
    
    examples = [
        "What is the average loan amount by loan type?",
        "Compare Q1 vs Q2 2024 default rates and explain what changed",
        "Why did loan defaults spike in Q2 2024? What were the root causes?",
        "Which province has the highest default rate and why?",
        "What factors correlate with higher default rates?",
        "What does our lending policy say about credit score requirements?",
        "Analyze the correlation between credit score and default rate",
        "What are the seasonal patterns in loan applications?",
    ]
    
    for i, example in enumerate(examples):
        if st.button(example, key=f"example_{i}"):
            st.session_state.current_query = example
    
    st.markdown("---")
    
    # Settings
    st.header("⚙️ Settings")
    st.session_state.show_reasoning = st.checkbox("Show reasoning steps", value=True)
    
    st.markdown("---")
    
    # Metrics
    st.header("📊 Session Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Queries", st.session_state.query_count)
    with col2:
        avg_time = st.session_state.total_duration / max(st.session_state.query_count, 1)
        st.metric("Avg Time", f"{avg_time:.1f}s")
    
    st.markdown("---")
    
    # About
    with st.expander("ℹ️ About This Agent"):
        st.markdown("""
        **Capabilities:**
        - Multi-step reasoning with LangGraph
        - RAG over internal documents
        - SQL query generation & execution
        - Statistical analysis with Python
        - Context-aware insights
        
        **Data Sources:**
        - 1K loan records (2022-2025)
        - 5K transaction records
        - 5 risk assessment reports (PDFs)
        
        **Tech Stack:**
        - LangGraph + LangChain
        - OpenAI GPT-4o-mini
        - ChromaDB (vector store)
        - SQLite + Pandas
        """)

# Main chat interface
st.header("💬 Chat")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if 'current_query' in st.session_state and st.session_state.current_query:
    query = st.session_state.current_query
    del st.session_state.current_query
else:
    query = st.chat_input("Ask a question about the financial data...")

if query:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    
    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Analyzing..."):
            start_time = time.time()
            
            try:
                result = st.session_state.agent.run(query)
                duration = time.time() - start_time
                
                # Update metrics
                st.session_state.query_count += 1
                st.session_state.total_duration += duration
                
                # Show reasoning steps if enabled
                if st.session_state.show_reasoning:
                    with st.expander("🔍 View Reasoning Steps", expanded=False):
                        # Planning
                        if result.get('analysis_plan'):
                            st.markdown("### 📋 Step 1: Planning")
                            st.info(result['analysis_plan'])
                        
                        # Document Search
                        if result.get('document_context') and 'No documents' not in result['document_context']:
                            st.markdown("### 📚 Step 2: Document Search")
                            doc_context = result['document_context']
                            if len(doc_context) > 800:
                                st.info(doc_context[:800] + "\n\n... (truncated for brevity)")
                            else:
                                st.info(doc_context)
                        
                        # SQL Execution
                        if result.get('sql_results'):
                            st.markdown("### 🔍 Step 3: SQL Query & Results")
                            sql_results = result['sql_results']
                            if len(sql_results) > 600:
                                st.code(sql_results[:600] + "\n... (truncated)", language="text")
                            else:
                                st.code(sql_results, language="text")
                        
                        # Analysis
                        if result.get('analysis_results'):
                            st.markdown("### 📊 Step 4: Statistical Analysis")
                            analysis = result['analysis_results']
                            if "Error in analysis" not in analysis:
                                if len(analysis) > 800:
                                    st.success(analysis[:800] + "...")
                                else:
                                    st.success(analysis)
                            else:
                                st.warning("Analysis step used SQL results directly (fallback)")
                        
                        # Metadata
                        st.markdown("### ⏱️ Execution Metrics")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Duration", f"{duration:.2f}s")
                        with col2:
                            st.metric("Steps Completed", 5)
                        with col3:
                            tokens = result.get('metadata', {}).get('estimated_tokens', 0)
                            st.metric("Est. Tokens", f"{tokens:,}" if tokens else "N/A")
                
                # Show final answer
                st.markdown(result['final_answer'])
                
                # Add feedback buttons
                col1, col2, col3 = st.columns([1, 1, 8])
                with col1:
                    if st.button("👍", key=f"up_{st.session_state.query_count}"):
                        st.success("Thanks!")
                with col2:
                    if st.button("👎", key=f"down_{st.session_state.query_count}"):
                        st.warning("Thanks for feedback!")
                
                # Store message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result['final_answer']
                })
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"I encountered an error: {str(e)}\n\nPlease try rephrasing your question."
                })

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**💼 Built by Stephen Torku **")
with col2:
    st.markdown("**🛠️ Tech:** LangGraph + RAG + GPT-4")
with col3:
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.session_state.total_duration = 0
        st.rerun()