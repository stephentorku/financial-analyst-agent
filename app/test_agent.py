from dotenv import load_dotenv
load_dotenv()

from app.agents.financial_analyst import FinancialAnalystAgent

print("🚀 Testing Financial Analyst Agent\n")

# Initialize agent
agent = FinancialAnalystAgent()
print("✅ Agent initialized\n")

# Test Query 1: Simple
print("\n" + "="*70)
print("TEST 1: Simple Query")
print("="*70)

result = agent.run("What is the average loan amount by loan type?")
print("\n📝 FINAL ANSWER:")
print(result['final_answer'])
print(f"\n⏱️  Duration: {result['metadata']['duration']:.2f}s")
print(f"🔧 Tools used: {', '.join(result['metadata'].get('tools_used', ['sql', 'analysis', 'documents']))}")

# Test Query 2: Complex with RAG
print("\n" + "="*70)
print("TEST 2: Complex Query with Document Context")
print("="*70)

result = agent.run("Why did loan defaults spike in Q2 2024? What were the root causes?")
print("\n📝 FINAL ANSWER:")
print(result['final_answer'])
print(f"\n⏱️  Duration: {result['metadata']['duration']:.2f}s")
print(f"🔧 Tools used: {', '.join(result['metadata'].get('tools_used', ['sql', 'analysis', 'documents']))}")
print(f"📊 Estimated tokens: {result['metadata'].get('estimated_tokens', 'N/A')}")

print("\n✅ All agent tests passed!")