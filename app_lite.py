"""
Lightweight Flask app - loads nothing at startup
Everything loads on-demand only when user asks first question
"""

from flask import Flask, render_template, request, jsonify
import os
import sys
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Global state
rag_instance = None
initialization_error = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    """For Render to check if app is alive"""
    return jsonify({'status': 'ok', 'message': 'App is running'}), 200

@app.route('/stats')
def stats():
    """Return stats - lightweight, no model loading"""
    if rag_instance:
        try:
            return jsonify({
                'total_chunks': rag_instance.collection.count(),
                'model': rag_instance.groq_model_name,
                'embedding_model': 'all-MiniLM-L6-v2',
                'top_k': rag_instance.top_k,
                'similarity_threshold': rag_instance.similarity_threshold
            })
        except:
            pass
    
    # Return defaults without loading anything
    return jsonify({
        'total_chunks': 129,
        'model': 'qwen/qwen3.8-27b',
        'embedding_model': 'all-MiniLM-L6-v2',
        'top_k': 5,
        'similarity_threshold': 0.1
    })

@app.route('/query', methods=['POST'])
def query():
    global rag_instance, initialization_error
    
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Please provide a question'}), 400
        
        # Initialize RAG only on first query
        if rag_instance is None:
            if initialization_error:
                return jsonify({
                    'error': f'System initialization failed: {initialization_error}. Please contact support.'
                }), 500
            
            try:
                print("First query - initializing RAG system...")
                sys.stdout.flush()
                
                from rag_system_groq import RAGSystem
                GROQ_API_KEY = os.getenv('GROQ_API_KEY')
                
                if not GROQ_API_KEY:
                    return jsonify({'error': 'API key not configured'}), 500
                
                print("Loading RAG components...")
                sys.stdout.flush()
                
                rag_instance = RAGSystem(
                    groq_api_key=GROQ_API_KEY,
                    similarity_threshold=0.1
                )
                
                print(f"RAG initialized successfully with {rag_instance.collection.count()} chunks")
                sys.stdout.flush()
                
            except Exception as e:
                error_msg = str(e)
                print(f"ERROR initializing RAG: {error_msg}")
                sys.stdout.flush()
                initialization_error = error_msg
                
                return jsonify({
                    'error': f'System initialization error: {error_msg}. This might be due to memory limits on free tier. Consider upgrading.'
                }), 500
        
        # Process query
        print(f"Processing query: {question[:50]}...")
        sys.stdout.flush()
        
        result = rag_instance.query(question, verbose=False)
        
        return jsonify({
            'answer': result.get('answer', 'No answer generated'),
            'sources': result.get('sources', []),
            'confidence': round(result.get('confidence', 0.0), 3),
            'latency': round(result.get('latency', 0.0), 2),
            'chunks_retrieved': result.get('retrieved_chunks', 0)
        })
    
    except Exception as e:
        error_msg = str(e)
        print(f"ERROR in query: {error_msg}")
        sys.stdout.flush()
        
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'error': f'Query error: {error_msg}'
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"Starting app on port {port}")
    print("RAG system will load on first query to save memory")
    sys.stdout.flush()
    app.run(debug=False, host='0.0.0.0', port=port)
