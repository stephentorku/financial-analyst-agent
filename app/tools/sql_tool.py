from langchain.tools import BaseTool
from typing import Optional
import sqlite3
import pandas as pd

class SQLQueryTool(BaseTool):
    name = "sql_query"
    description = """
    Execute SQL queries on the banking database.
    Available tables: 
    - loans: loan_id, application_date, loan_type, amount, interest_rate, term_months, 
             credit_score, province, customer_age, income, employment_status, defaulted, days_past_due
    - transactions: transaction_id, timestamp, customer_id, type, amount, merchant, is_fraud
    
    Input should be a valid SQL query string.
    Returns: Query results as a formatted string
    """
    
    def _run(self, query: str) -> str:
        try:
            conn = sqlite3.connect('app/data/structured/banking.db')
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if df.empty:
                return "Query returned no results."
            
            # Format for LLM consumption
            result = f"Query executed successfully. Returned {len(df)} rows.\n\n"
            result += df.to_string(index=False, max_rows=100)
            
            return result
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        return self._run(query)