from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from typing import TypedDict, List, Annotated, Dict, Any
import operator
from tools.sql_tool import SQLQueryTool
from tools.analysis_tool import DataAnalysisTool
from tools.visualization_tool import VisualizationTool
from tools.document_search_tool import DocumentSearchTool
from dotenv import load_dotenv
import uuid
import time

load_dotenv()


class AgentState(TypedDict):
    """State that gets passed between nodes"""
    messages: Annotated[List[Dict[str, str]], operator.add]
    query: str
    run_id: str
    analysis_plan: str
    document_context: str
    sql_results: str
    analysis_results: str
    visualization: str
    final_answer: str
    metadata: Dict[str, Any]


class FinancialAnalystAgent:
    def __init__(self, model_name="gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.tools = {
            'sql': SQLQueryTool(),
            'analysis': DataAnalysisTool(),
            'viz': VisualizationTool(),
            'docs': DocumentSearchTool()
        }
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Define nodes (each step in the reasoning process)
        workflow.add_node("planner", self.plan_analysis)
        workflow.add_node("doc_searcher", self.search_documents)
        workflow.add_node("sql_executor", self.execute_sql)
        workflow.add_node("analyzer", self.analyze_data)
        workflow.add_node("synthesizer", self.synthesize_answer)
        
        # Define edges (flow between steps)
        workflow.set_entry_point("planner")
        workflow.add_edge("planner", "doc_searcher")
        workflow.add_edge("doc_searcher", "sql_executor")
        workflow.add_edge("sql_executor", "analyzer")
        workflow.add_edge("analyzer", "synthesizer")
        workflow.add_edge("synthesizer", END)
        
        return workflow.compile()
    
    def plan_analysis(self, state: AgentState) -> AgentState:
        """Step 1: Plan the analysis approach"""
        print("📋 Planning analysis...")
        
        prompt = f"""You are a financial data analyst planning how to answer this question.

User query: {state['query']}

Create a step-by-step analysis plan. Include:
1. What data tables/columns to query (loans, transactions tables available)
2. What calculations/statistics to compute
3. What insights to look for
4. What context from documents might be relevant

Be specific and actionable. Keep it concise (3-5 steps)."""

        response = self.llm.invoke([
            SystemMessage(content="You are an expert financial analyst."),
            HumanMessage(content=prompt)
        ])
        
        state['analysis_plan'] = response.content
        state['messages'].append({
            "role": "assistant",
            "step": "planning",
            "content": f"**Analysis Plan:**\n{response.content}"
        })
        
        return state
    
    def search_documents(self, state: AgentState) -> AgentState:
        """Step 2: Search for relevant context in documents"""
        print("📚 Searching internal documents...")
        
        prompt = f"""Based on this query: {state['query']}

And this analysis plan: {state['analysis_plan']}

What should we search for in our internal risk reports, lending policies, and economic outlooks?
Provide a concise search query (3-7 words) to find relevant context about WHY trends might have occurred."""

        response = self.llm.invoke([
            SystemMessage(content="You are a research assistant."),
            HumanMessage(content=prompt)
        ])
        
        search_query = response.content.strip()
        print(f"   Searching for: {search_query}")
        
        # Execute document search
        doc_results = self.tools['docs']._run(search_query)
        
        state['document_context'] = doc_results
        state['messages'].append({
            "role": "assistant",
            "step": "document_search",
            "content": f"**Document Search:** {search_query}\n\nFound relevant context in internal documents."
        })
        
        return state
    
    def execute_sql(self, state: AgentState) -> AgentState:
        """Step 3: Execute SQL queries to get data"""
        print("🔍 Executing SQL query...")
        
        prompt = f"""Based on this analysis plan:
{state['analysis_plan']}

Available tables and columns:
- loans: loan_id, application_date, loan_type, amount, interest_rate, term_months, 
         credit_score, province, customer_age, income, employment_status, defaulted, days_past_due
- transactions: transaction_id, timestamp, customer_id, type, amount, merchant, is_fraud

Write a SQL query to get the necessary data. 
IMPORTANT: 
- Use proper date formatting: BETWEEN '2024-01-01' AND '2024-12-31'
- Include aggregations where appropriate (AVG, COUNT, SUM)
- Keep it focused on the user's question

Provide ONLY the SQL query, nothing else."""

        response = self.llm.invoke([
            SystemMessage(content="You are a SQL expert. Return only valid SQL queries."),
            HumanMessage(content=prompt)
        ])
        
        # Clean up the SQL query
        sql_query = response.content.strip()
        sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
        
        print(f"   Query: {sql_query[:100]}...")
        
        # Execute the query
        results = self.tools['sql']._run(sql_query)
        
        state['sql_results'] = results
        state['messages'].append({
            "role": "assistant",
            "step": "sql_execution",
            "content": f"**SQL Query:**\n```sql\n{sql_query}\n```\n\n**Results:** Retrieved data successfully."
        })
        
        return state
    
    def analyze_data(self, state: AgentState) -> AgentState:
        """Step 4: Perform statistical analysis"""
        print("📊 Performing statistical analysis...")
        
        prompt = f"""Based on these SQL results:
    {state['sql_results'][:1000]}

    And this plan:
    {state['analysis_plan']}

    Write Python code using pandas and numpy to compute relevant statistics, trends, or comparisons.
    You have access to:
    - loans_df: DataFrame with columns: loan_id, application_date, loan_type, amount, interest_rate, 
    term_months, credit_score, province, customer_age, income, employment_status, defaulted, days_past_due
    - transactions_df: DataFrame with columns: transaction_id, timestamp, customer_id, type, amount, merchant, is_fraud

    CRITICAL - Use EXACT column names:
    - For loans: 'defaulted' (not 'default_status'), 'amount' (not 'loan_amount')
    - For transactions: 'amount' (not 'payment_amount')

    IMPORTANT:
    - Store the final result in a variable called 'result'
    - Make 'result' a clear, formatted string with key findings
    - Include percentages, comparisons, trends
    - Keep it concise but informative
    - If SQL results already answer the question, just summarize them

    Provide ONLY Python code, nothing else."""

        response = self.llm.invoke([
            SystemMessage(content="You are a Python data analysis expert."),
            HumanMessage(content=prompt)
        ])
        
        # Clean up code
        code = response.content.strip()
        code = code.replace('```python', '').replace('```', '').strip()
        
        print(f"   Executing analysis code...")
        
        # Execute analysis
        try:
            analysis_results = self.tools['analysis']._run(code)
            
            # If analysis failed but we have SQL results, use those
            if "Error in analysis" in analysis_results and state['sql_results']:
                analysis_results = "Using SQL results directly: " + state['sql_results'][:500]
                
        except Exception as e:
            # Fallback: use SQL results if analysis fails
            analysis_results = f"Analysis step skipped. Using SQL results: {state['sql_results'][:500]}"
        
        state['analysis_results'] = analysis_results
        state['messages'].append({
            "role": "assistant",
            "step": "analysis",
            "content": f"**Statistical Analysis:**\n{analysis_results}"
        })
        
        return state
    
    def synthesize_answer(self, state: AgentState) -> AgentState:
        """Step 5: Synthesize comprehensive answer"""
        print("✨ Synthesizing final answer...")
        
        prompt = f"""User asked: {state['query']}

You have gathered the following information:

ANALYSIS PLAN:
{state['analysis_plan']}

CONTEXT FROM INTERNAL DOCUMENTS:
{state['document_context'][:2000]}

SQL RESULTS:
{state['sql_results'][:1000]}

STATISTICAL ANALYSIS:
{state['analysis_results']}

Now provide a comprehensive answer that:
1. **Directly answers the user's question** (lead with the answer)
2. **Highlights key findings** with specific numbers
3. **Explains WHY** using context from internal documents
4. **Provides actionable insights** or recommendations

Format:
- Use clear paragraphs
- Bold key findings
- Be conversational but professional
- Cite document sources when using their context (e.g., "According to our Q2 2024 Risk Report...")

Keep it concise (200-300 words) but comprehensive."""

        response = self.llm.invoke([
            SystemMessage(content="You are a senior financial analyst presenting findings to business stakeholders."),
            HumanMessage(content=prompt)
        ])
        
        state['final_answer'] = response.content
        state['messages'].append({
            "role": "assistant",
            "step": "final_answer",
            "content": response.content
        })
        
        return state
    
    def run(self, query: str) -> dict:
        """Run the agent on a query"""
        print(f"\n{'='*60}")
        print(f"🤖 Processing Query: {query}")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        run_id = str(uuid.uuid4())
        
        initial_state = {
            "messages": [],
            "query": query,
            "run_id": run_id,
            "analysis_plan": "",
            "document_context": "",
            "sql_results": "",
            "analysis_results": "",
            "visualization": "",
            "final_answer": "",
            "metadata": {
                "start_time": start_time,
                "model": "gpt-4o-mini"
            }
        }
        
        try:
            final_state = self.graph.invoke(initial_state)
            
            duration = time.time() - start_time
            final_state['metadata']['duration'] = duration
            final_state['metadata']['success'] = True
            
            print(f"\n✅ Analysis complete in {duration:.2f}s")
            print(f"{'='*60}\n")
            
            return final_state
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            initial_state['metadata']['success'] = False
            initial_state['metadata']['error'] = str(e)
            raise