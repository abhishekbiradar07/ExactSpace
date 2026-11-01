"""
Flask Web Frontend for RAG System
Simple web interface to query the RAG system
Memory optimized for Render free tier
"""

from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Lazy load RAG system only when needed
rag = None

def get_rag():
    """Lazy initialization of RAG system"""
    global rag
    if rag is None:
        from rag_system_groq import RAGSystem
        GROQ_API_KEY = os.getenv('GROQ_API_KEY')
        rag = RAGSystem(groq_api_key=GROQ_API_KEY, similarity_threshold=0.1)
        print(f"RAG System loaded with {rag.collection.count()} chunks")
    return rag

@app.route('/')
def home():
    """Render main page"""
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    """Handle query request"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                'error': 'Please provide a question'
            }), 400
        
        rag_system = get_rag()
        result = rag_system.query(question, verbose=False)
        
        # Ensure all required fields are present
        response_data = {
            'answer': result.get('answer', 'No answer generated'),
            'sources': result.get('sources', []),
            'confidence': round(result.get('confidence', 0.0), 3),
            'latency': round(result.get('latency', 0.0), 2),
            'chunks_retrieved': result.get('retrieved_chunks', 0)
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Error processing query: {str(e)}'
        }), 500

@app.route('/stats')
def stats():
    """Get system statistics"""
    try:
        rag_system = get_rag()
        return jsonify({
            'total_chunks': rag_system.collection.count(),
            'model': rag_system.groq_model_name,
            'embedding_model': 'all-MiniLM-L6-v2',
            'top_k': rag_system.top_k,
            'similarity_threshold': rag_system.similarity_threshold
        })
    except Exception as e:
        # Return default stats if RAG not initialized yet
        return jsonify({
            'total_chunks': 129,
            'model': 'qwen/qwen3.8-27b',
            'embedding_model': 'all-MiniLM-L6-v2',
            'top_k': 5,
            'similarity_threshold': 0.1
        })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("RAG SYSTEM WEB INTERFACE")
    print("="*60)
    print("Starting server...")
    print("="*60 + "\n")
    
    # Get port from environment variable (for Render/Heroku)
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
