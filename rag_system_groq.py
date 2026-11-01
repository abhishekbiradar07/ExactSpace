"""
Production RAG System with Groq API
Uses free, fast models from Groq
"""

import os
import warnings
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
import time

import numpy as np
import pandas as pd
from tqdm import tqdm

# PDF processing
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

# Embeddings
from sentence_transformers import SentenceTransformer

# Vector DB
import chromadb
from chromadb.config import Settings

# Groq API
from groq import Groq

warnings.filterwarnings('ignore')


class RAGSystem:
    """
    Production RAG system with Groq API for generation
    """
    
    def __init__(
        self,
        groq_api_key: str,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        groq_model: str = "qwen/qwen3.8-27b",
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        top_k: int = 5,
        similarity_threshold: float = 0.3,
        vector_store_path: str = "./vector_store"
    ):
        """
        Initialize RAG system
        
        Args:
            groq_api_key: Groq API key
            embedding_model: HuggingFace model for embeddings
            groq_model: Groq model name (llama-3.3-70b-versatile, mixtral-8x7b-32768, etc)
            chunk_size: Number of tokens per chunk
            chunk_overlap: Token overlap between chunks
            top_k: Number of chunks to retrieve
            similarity_threshold: Minimum similarity for relevance
            vector_store_path: Path to store vector database
        """
        print("Initializing RAG System with Groq...")
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
        self.vector_store_path = vector_store_path
        
        # Configure Groq
        print(f"Configuring Groq API ({groq_model})...")
        self.groq_client = Groq(api_key=groq_api_key)
        self.groq_model_name = groq_model
        
        # Test Groq connection
        try:
            test_response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": "test"}],
                model=groq_model,
                max_tokens=10
            )
            print("Groq API connected successfully")
        except Exception as e:
            print(f"Warning: Groq API test failed: {e}")
        
        # Load embedding model
        print(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Initialize ChromaDB
        print(f"Initializing vector database at {vector_store_path}")
        self.chroma_client = chromadb.PersistentClient(path=vector_store_path)
        
        try:
            self.collection = self.chroma_client.get_collection("technical_docs")
            print(f"Loaded existing collection with {self.collection.count()} chunks")
        except:
            self.collection = self.chroma_client.create_collection(
                name="technical_docs",
                metadata={"description": "Technical documentation chunks"}
            )
            print("Created new collection")
        
        print("RAG System initialized successfully\n")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        if PyPDF2 is None:
            raise ImportError("PyPDF2 not installed. Run: pip install PyPDF2")
        
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n\n--- Page {page_num + 1} ---\n\n{page_text}"
        except Exception as e:
            print(f"Error reading {pdf_path}: {e}")
        
        return text
    
    def chunk_text(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunk text with overlap"""
        words = text.split()
        chunks = []
        
        words_per_chunk = int(self.chunk_size * 0.75)
        words_overlap = int(self.chunk_overlap * 0.75)
        
        for i in range(0, len(words), words_per_chunk - words_overlap):
            chunk_words = words[i:i + words_per_chunk]
            chunk_text = " ".join(chunk_words)
            
            if len(chunk_text.strip()) > 50:
                chunk_metadata = metadata.copy()
                chunk_metadata['chunk_index'] = len(chunks)
                chunk_metadata['char_start'] = len(" ".join(words[:i]))
                chunk_metadata['char_end'] = chunk_metadata['char_start'] + len(chunk_text)
                
                chunks.append({
                    'text': chunk_text,
                    'metadata': chunk_metadata
                })
        
        return chunks
    
    def ingest_documents(self, docs_folder: str):
        """Ingest all PDF documents from folder"""
        print(f"Ingesting documents from: {docs_folder}")
        
        docs_path = Path(docs_folder)
        if not docs_path.exists():
            print(f"Folder not found: {docs_folder}")
            return
        
        pdf_files = list(docs_path.glob("*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {docs_folder}")
            return
        
        print(f"Found {len(pdf_files)} PDF files")
        
        all_chunks = []
        
        for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
            text = self.extract_text_from_pdf(str(pdf_file))
            
            if not text.strip():
                print(f"No text extracted from {pdf_file.name}")
                continue
            
            metadata = {
                'source': pdf_file.name,
                'file_path': str(pdf_file)
            }
            chunks = self.chunk_text(text, metadata)
            all_chunks.extend(chunks)
            
            print(f"  {pdf_file.name}: {len(chunks)} chunks")
        
        if not all_chunks:
            print("No chunks created. Check your PDF files.")
            return
        
        print(f"\nGenerating embeddings for {len(all_chunks)} chunks...")
        
        texts = [chunk['text'] for chunk in all_chunks]
        embeddings = self.embedding_model.encode(
            texts,
            show_progress_bar=True,
            batch_size=32
        )
        
        print("Adding to vector database...")
        
        ids = [f"chunk_{i}" for i in range(len(all_chunks))]
        metadatas = [chunk['metadata'] for chunk in all_chunks]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=metadatas
        )
        
        print(f"Ingestion complete! Total chunks in database: {self.collection.count()}\n")
    
    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve relevant chunks for query"""
        query_embedding = self.embedding_model.encode([query])[0]
        
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=self.top_k
        )
        
        retrieved_chunks = []
        
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                chunk = {
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'similarity': 1 - results['distances'][0][i] if 'distances' in results else 1.0
                }
                retrieved_chunks.append(chunk)
        
        return retrieved_chunks
    
    def generate_answer(self, query: str, context_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate answer using Groq with retrieved context"""
        if not context_chunks:
            return {
                'answer': "I couldn't find relevant information in the documentation to answer your question.",
                'confidence': 0.0,
                'sources': [],
                'retrieved_chunks': 0
            }
        
        avg_similarity = np.mean([chunk['similarity'] for chunk in context_chunks])
        
        # Always generate an answer if we have context chunks, even with low similarity
        # The confidence score will inform the user about reliability
        
        # Build context
        context = "\n\n".join([
            f"[Source: {chunk['metadata']['source']}]\n{chunk['text']}"
            for chunk in context_chunks
        ])
        
        # Create prompt
        prompt = f"""You are a helpful technical assistant answering questions about cyclone separator equipment and documentation.

Context from documentation:
{context}

Question: {query}

Instructions:
- Answer the question based on the provided context in a clear, conversational manner
- Use simple language and proper formatting (paragraphs, bullet points, numbered lists)
- Break down complex information into easy-to-understand sections
- Cite source documents naturally (e.g., "According to the Cyclone Manual...")
- Even if the context is somewhat related but not perfect, provide the most relevant information available
- If some aspects are unclear from the context, answer what you can and mention what's not covered
- Be helpful and informative

Answer:"""
        
        # Generate with Groq
        try:
            response = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a knowledgeable technical assistant who explains complex topics in a clear, well-structured, and human-friendly way. Use proper formatting with paragraphs, bullet points, and clear sections. Always cite sources naturally in your explanations."},
                    {"role": "user", "content": prompt}
                ],
                model=self.groq_model_name,
                max_tokens=800,
                temperature=0.3
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating answer: {e}")
            answer = "Error generating answer. Please try again."
        
        sources = list(set([chunk['metadata']['source'] for chunk in context_chunks]))
        
        return {
            'answer': answer,
            'confidence': float(avg_similarity),
            'sources': sources,
            'retrieved_chunks': len(context_chunks)
        }
    
    def query(self, question: str, verbose: bool = True) -> Dict[str, Any]:
        """Complete RAG query pipeline"""
        start_time = time.time()
        
        if verbose:
            print(f"Query: {question}\n")
        
        retrieved_chunks = self.retrieve(question)
        
        if verbose:
            print(f"Retrieved {len(retrieved_chunks)} chunks")
            if retrieved_chunks:
                print(f"Top similarity: {retrieved_chunks[0]['similarity']:.3f}\n")
        
        result = self.generate_answer(question, retrieved_chunks)
        
        elapsed_time = time.time() - start_time
        result['latency'] = elapsed_time
        
        if verbose:
            print(f"Answer: {result['answer']}\n")
            print(f"Sources: {', '.join(result['sources'])}")
            print(f"Confidence: {result['confidence']:.3f}")
            print(f"Time: {elapsed_time:.2f}s\n")
        
        return result
    
    def evaluate(self, queries_file: str = "evaluation_queries.csv", output_file: str = "evaluation_results.csv"):
        """Evaluate system on test queries"""
        print(f"Running evaluation...")
        
        if not os.path.exists(queries_file):
            print(f"Queries file not found: {queries_file}")
            print("Creating sample queries file...")
            self._create_sample_queries(queries_file)
        
        df = pd.read_csv(queries_file)
        results = []
        
        for idx, row in tqdm(df.iterrows(), total=len(df), desc="Evaluating"):
            query = row['query']
            result = self.query(query, verbose=False)
            
            results.append({
                'query': query,
                'answer': result['answer'],
                'sources': ', '.join(result['sources']),
                'confidence': result['confidence'],
                'latency': result['latency'],
                'chunks_retrieved': result['retrieved_chunks']
            })
        
        results_df = pd.DataFrame(results)
        results_df.to_csv(output_file, index=False)
        
        avg_confidence = results_df['confidence'].mean()
        avg_latency = results_df['latency'].mean()
        
        print(f"\nEvaluation Results:")
        print(f"  Total queries: {len(results_df)}")
        print(f"  Avg confidence: {avg_confidence:.3f}")
        print(f"  Avg latency: {avg_latency:.2f}s")
        print(f"  Results saved to: {output_file}\n")
    
    def _create_sample_queries(self, filename: str):
        """Create sample evaluation queries"""
        sample_queries = [
            "What does a sudden draft drop indicate?",
            "How do I troubleshoot a pressure sensor failure?",
            "What are the safety procedures for emergency shutdown?",
            "Explain the startup sequence",
            "What is the recommended maintenance schedule?",
        ]
        
        df = pd.DataFrame({'query': sample_queries})
        df.to_csv(filename, index=False)
        print(f"Created sample queries file: {filename}")


def main():
    """Main function for CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="RAG System for Technical Documentation")
    parser.add_argument('--api-key', type=str, help='Groq API key (or set GROQ_API_KEY env var)')
    parser.add_argument('--ingest', type=str, help='Folder containing PDF documents to ingest')
    parser.add_argument('--query', type=str, help='Query to ask the system')
    parser.add_argument('--evaluate', action='store_true', help='Run evaluation')
    parser.add_argument('--interactive', action='store_true', help='Interactive query mode')
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("Error: Groq API key required")
        print("Provide via --api-key argument or GROQ_API_KEY environment variable")
        print("Get free API key from: https://console.groq.com/keys")
        return
    
    rag = RAGSystem(groq_api_key=api_key)
    
    if args.ingest:
        rag.ingest_documents(args.ingest)
    
    if args.query:
        rag.query(args.query)
    
    if args.evaluate:
        rag.evaluate()
    
    if args.interactive:
        print("Interactive mode. Type 'exit' to quit.\n")
        while True:
            query = input("Your question: ").strip()
            if query.lower() in ['exit', 'quit', 'q']:
                break
            if query:
                rag.query(query)
    
    if not any([args.ingest, args.query, args.evaluate, args.interactive]):
        parser.print_help()
        print("\nQuick start:")
        print("  1. Get API key: https://console.groq.com/keys")
        print("  2. Set: export GROQ_API_KEY='your-key'")
        print("  3. Ingest: python rag_system_groq.py --ingest docs/")
        print("  4. Query: python rag_system_groq.py --interactive")


if __name__ == "__main__":
    main()
