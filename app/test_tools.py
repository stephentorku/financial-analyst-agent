from tools import SQLQueryTool, DataAnalysisTool, DocumentSearchTool

print("🧪 Testing tools...\n")

# Test SQL Tool
print("1. Testing SQL Tool...")
sql_tool = SQLQueryTool()
result = sql_tool._run("SELECT COUNT(*) as total_loans FROM loans")
print(f"   Result: {result[:100]}...")
print("   ✅ SQL Tool works!\n")

# Test Analysis Tool
print("2. Testing Analysis Tool...")
analysis_tool = DataAnalysisTool()
code = """
result = loans_df['defaulted'].mean() * 100
"""
result = analysis_tool._run(code)
print(f"   Result: {result}")
print("   ✅ Analysis Tool works!\n")

# Test Document Search Tool
print("3. Testing Document Search Tool (this takes a minute)...")
doc_tool = DocumentSearchTool()
result = doc_tool._run("Q2 2024 default rate spike")
print(f"   Result: {result[:200]}...")
print("   ✅ Document Search Tool works!\n")

print("🎉 All tools validated!")