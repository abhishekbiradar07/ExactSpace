"""
Test the RAG system locally before deploying
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing RAG System Locally...")
print("="*60)

# Check environment
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    print("❌ GROQ_API_KEY not found in .env")
    exit(1)
else:
    print(f"✓ API Key found: {api_key[:20]}...")

# Test import
try:
    from rag_system_groq import RAGSystem
    print("✓ RAG system imports successfully")
except Exception as e:
    print(f"❌ Import error: {e}")
    exit(1)

# Test initialization
try:
    print("\nInitializing RAG system...")
    rag = RAGSystem(groq_api_key=api_key, similarity_threshold=0.1)
    print(f"✓ RAG initialized with {rag.collection.count()} chunks")
except Exception as e:
    print(f"❌ Initialization error: {e}")
    exit(1)

# Test query
try:
    print("\nTesting query...")
    result = rag.query("How does a cyclone separator work?", verbose=False)
    print(f"✓ Query successful!")
    print(f"  Answer length: {len(result['answer'])} chars")
    print(f"  Confidence: {result['confidence']:.3f}")
    print(f"  Sources: {len(result['sources'])}")
    print(f"  Time: {result['latency']:.2f}s")
except Exception as e:
    print(f"❌ Query error: {e}")
    exit(1)

print("\n" + "="*60)
print("✓ All tests passed! System is working locally.")
print("\nYou can now run the web server:")
print("  python app.py")
print("\nOr test with gunicorn:")
print("  gunicorn -c gunicorn_config.py app:app")
