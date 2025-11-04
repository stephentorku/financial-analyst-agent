from langchain.tools import BaseTool
import pandas as pd
import numpy as np
from typing import Dict, Any
import sqlite3

class DataAnalysisTool(BaseTool):
    name = "data_analysis"
    description = """
    Perform statistical analysis and computations on data.
    Input should be a Python code string that uses pandas and numpy.
    The code can access 'loans_df' and 'transactions_df' dataframes.
    Store the final result in a variable called 'result'.
    Returns: Analysis results as string
    """
    
    def _run(self, code: str) -> str:
        try:
            # Load data
            conn = sqlite3.connect('app/data/structured/banking.db')
            loans_df = pd.read_sql_query("SELECT * FROM loans", conn)
            transactions_df = pd.read_sql_query("SELECT * FROM transactions", conn)
            conn.close()
            
            # Parse dates
            loans_df['application_date'] = pd.to_datetime(loans_df['application_date'])
            transactions_df['timestamp'] = pd.to_datetime(transactions_df['timestamp'])
            
            # Execute code in controlled namespace
            namespace = {
                'pd': pd,
                'np': np,
                'loans_df': loans_df,
                'transactions_df': transactions_df
            }
            
            exec(code, namespace)
            
            # Capture 'result' variable from executed code
            if 'result' in namespace:
                return str(namespace['result'])
            else:
                return "Code executed but no 'result' variable was set."
                
        except Exception as e:
            return f"Error in analysis: {str(e)}"
    
    async def _arun(self, code: str) -> str:
        return self._run(code)