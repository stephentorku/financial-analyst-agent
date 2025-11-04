from langchain.tools import BaseTool
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3
import os
from typing import Dict

class VisualizationTool(BaseTool):
    name = "create_visualization"
    description = """
    Create visualizations from data analysis.
    Input: JSON string with: {"type": "line|bar|scatter|pie", "data_query": "SQL query", "x": "column", "y": "column", "title": "title"}
    Returns: Path to saved visualization
    """
    
    def _run(self, viz_spec: str) -> str:
        try:
            import json
            spec = json.loads(viz_spec)
            
            # Get data
            conn = sqlite3.connect('app/data/structured/banking.db')
            df = pd.read_sql_query(spec['data_query'], conn)
            conn.close()
            
            # Create visualization
            viz_type = spec.get('type', 'bar')
            
            if viz_type == 'line':
                fig = px.line(df, x=spec['x'], y=spec['y'], title=spec.get('title', ''))
            elif viz_type == 'bar':
                fig = px.bar(df, x=spec['x'], y=spec['y'], title=spec.get('title', ''))
            elif viz_type == 'scatter':
                fig = px.scatter(df, x=spec['x'], y=spec['y'], title=spec.get('title', ''))
            elif viz_type == 'pie':
                fig = px.pie(df, names=spec['x'], values=spec['y'], title=spec.get('title', ''))
            
            # Save
            os.makedirs('app/data/visualizations', exist_ok=True)
            path = f"app/data/visualizations/{spec.get('title', 'chart').replace(' ', '_')}.html"
            fig.write_html(path)
            
            return f"Visualization saved to {path}"
            
        except Exception as e:
            return f"Error creating visualization: {str(e)}"
    
    async def _arun(self, viz_spec: str) -> str:
        return self._run(viz_spec)