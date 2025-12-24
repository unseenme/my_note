"""
RAG (Retrieval Augmented Generation) Module
Implements vector-based similarity search
"""

import numpy as np
from typing import List, Dict, Tuple
from knowledge_base import KnowledgeBase
from config import Config


class RAGRetriever:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.embeddings_cache = {}
    
    def _simple_embedding(self, text: str) -> np.ndarray:
        """
        Simple embedding using character n-grams and word frequency
        In production, use OpenAI embeddings or sentence-transformers
        """
        # Check cache
        if text in self.embeddings_cache:
            return self.embeddings_cache[text]
        
        # Normalize text
        text = text.lower()
        words = text.split()
        
        # Create a simple bag-of-words vector (300 dimensions)
        vector = np.zeros(300)
        
        # Word-level features
        for i, word in enumerate(words[:100]):  # Limit to first 100 words
            # Hash word to dimension
            hash_val = hash(word) % 300
            vector[hash_val] += 1.0 / (i + 1)  # Weight by position
        
        # Character n-gram features
        for n in [2, 3]:
            for i in range(len(text) - n + 1):
                ngram = text[i:i+n]
                hash_val = hash(ngram) % 300
                vector[hash_val] += 0.5
        
        # Normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        # Cache the result
        self.embeddings_cache[text] = vector
        return vector
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """Compute cosine similarity between two texts"""
        emb1 = self._simple_embedding(text1)
        emb2 = self._simple_embedding(text2)
        
        # Cosine similarity
        similarity = np.dot(emb1, emb2)
        return float(similarity)
    
    def retrieve(self, query: str, top_k: int = None) -> List[Tuple[Dict, float]]:
        """
        Retrieve relevant FAQs based on query
        Returns: List of (faq, similarity_score) tuples
        """
        if top_k is None:
            top_k = Config.RAG_TOP_K
        
        # Get all FAQs
        faqs = self.kb.get_verified_faqs()
        if not faqs:
            faqs = self.kb.faqs
        
        # Compute similarities
        similarities = []
        for faq in faqs:
            score = self.compute_similarity(query, faq['question'])
            similarities.append((faq, score))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Filter by threshold and return top_k
        results = [
            (faq, score) for faq, score in similarities 
            if score >= Config.RAG_SIMILARITY_THRESHOLD
        ]
        
        return results[:top_k]
    
    def format_context(self, retrieved_items: List[Tuple[Dict, float]]) -> str:
        """Format retrieved FAQs as context for LLM"""
        if not retrieved_items:
            return "No relevant information found in knowledge base."
        
        context_parts = ["### Relevant Knowledge Base Entries:\n"]
        for i, (faq, score) in enumerate(retrieved_items, 1):
            context_parts.append(
                f"{i}. [Source: FAQ-{faq['id']}, Relevance: {score:.2f}]\n"
                f"   Q: {faq['question']}\n"
                f"   A: {faq['answer']}\n"
            )
        
        return "\n".join(context_parts)
    
    def get_sources(self, retrieved_items: List[Tuple[Dict, float]]) -> List[str]:
        """Extract source references for citation"""
        return [f"FAQ-{faq['id']}" for faq, _ in retrieved_items]
