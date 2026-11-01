"""
Minimal Flask Frontend for RAG System - Optimized for 512MB RAM
"""

from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Global variable for RAG system
rag = None
rag_loading = False

def get_rag():
    """Lazy initialization with memory optimization"""
    global rag, rag_loading
    
    if rag is not None:
        return rag
    
    if rag_loading:
        raise Exception("RAG system is currently loading, please try again in a moment")
    
    rag_loading = True
    try:
        from rag_system_groq import RAGSystem
        GROQ_API_KEY = os.getenv('GROQ_API_KEY')
        rag = RAGSystem(groq_api_key=GROQ_API_KEY, similarity_threshold=0.1)
        print(f"RAG System loaded with {rag.collection.count()} chunks")
        return rag
    finally:
        rag_loading = False

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
        
        try:
            rag_system = get_rag()
        except Exception as e:
            return jsonify({
                'error': 'System is initializing, please wait a moment and try again'
            }), 503
        
        result = rag_system.query(question, verbose=False)
        
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
            'error': f'Error: {str(e)}'
        }), 500

@app.route('/stats')
def stats():
    """Get system statistics"""
    try:
        if rag is not None:
            return jsonify({
                'total_chunks': rag.collection.count(),
                'model': rag.groq_model_name,
                'embedding_model': 'all-MiniLM-L6-v2',
                'top_k': rag.top_k,
                'similarity_threshold': rag.similarity_threshold,
                'status': 'ready'
            })
        else:
            return jsonify({
                'total_chunks': 129,
                'model': 'qwen/qwen3.8-27b',
                'embedding_model': 'all-MiniLM-L6-v2',
                'top_k': 5,
                'similarity_threshold': 0.1,
                'status': 'not_initialized'
            })
    except Exception as e:
        return jsonify({
            'total_chunks': 129,
            'model': 'qwen/qwen3.8-27b',
            'embedding_model': 'all-MiniLM-L6-v2',
            'top_k': 5,
            'similarity_threshold': 0.1,
            'status': 'error',
            'error': str(e)
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
