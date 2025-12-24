"""
Knowledge Base Management Module
Handles FAQ and document storage/retrieval
"""

import json
import numpy as np
from typing import List, Dict, Optional


class KnowledgeBase:
    def __init__(self, faq_file: str = "data/faq.json"):
        self.faq_file = faq_file
        self.faqs: List[Dict] = []
        self.embeddings: Optional[np.ndarray] = None
        self._load_faqs()
    
    def _load_faqs(self):
        """Load FAQs from JSON file"""
        try:
            with open(self.faq_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.faqs = data.get('faqs', [])
                print(f"Loaded {len(self.faqs)} FAQs")
        except FileNotFoundError:
            print(f"FAQ file not found: {self.faq_file}")
            self._create_default_faqs()
    
    def _create_default_faqs(self):
        """Create default FAQ data"""
        self.faqs = [
            {
                "id": 1,
                "question": "What are your business hours?",
                "answer": "We are open Monday to Friday, 9 AM to 6 PM (GMT+8).",
                "category": "general",
                "verified": True
            },
            {
                "id": 2,
                "question": "How do I reset my password?",
                "answer": "Click 'Forgot Password' on the login page, enter your email, and follow the instructions sent to your inbox.",
                "category": "account",
                "verified": True
            },
            {
                "id": 3,
                "question": "What payment methods do you accept?",
                "answer": "We accept credit cards (Visa, MasterCard, AMEX), PayPal, and bank transfers.",
                "category": "payment",
                "verified": True
            },
            {
                "id": 4,
                "question": "How long does shipping take?",
                "answer": "Standard shipping takes 3-5 business days. Express shipping takes 1-2 business days.",
                "category": "shipping",
                "verified": True
            },
            {
                "id": 5,
                "question": "What is your return policy?",
                "answer": "We accept returns within 30 days of purchase. Items must be unused and in original packaging.",
                "category": "returns",
                "verified": True
            }
        ]
        # Save default FAQs
        self.save_faqs()
    
    def save_faqs(self):
        """Save FAQs to JSON file"""
        import os
        os.makedirs('data', exist_ok=True)
        with open(self.faq_file, 'w', encoding='utf-8') as f:
            json.dump({'faqs': self.faqs}, f, ensure_ascii=False, indent=2)
    
    def add_faq(self, question: str, answer: str, category: str, verified: bool = False):
        """Add new FAQ entry"""
        faq_id = max([faq['id'] for faq in self.faqs], default=0) + 1
        new_faq = {
            'id': faq_id,
            'question': question,
            'answer': answer,
            'category': category,
            'verified': verified
        }
        self.faqs.append(new_faq)
        self.save_faqs()
        # Reset embeddings to force recalculation
        self.embeddings = None
    
    def get_all_questions(self) -> List[str]:
        """Get all questions for embedding"""
        return [faq['question'] for faq in self.faqs]
    
    def get_faq_by_id(self, faq_id: int) -> Optional[Dict]:
        """Get FAQ by ID"""
        for faq in self.faqs:
            if faq['id'] == faq_id:
                return faq
        return None
    
    def get_verified_faqs(self) -> List[Dict]:
        """Get only verified FAQs (to avoid AI hallucination)"""
        return [faq for faq in self.faqs if faq.get('verified', False)]
    
    def search_by_keyword(self, keyword: str) -> List[Dict]:
        """Simple keyword search"""
        keyword_lower = keyword.lower()
        results = []
        for faq in self.faqs:
            if (keyword_lower in faq['question'].lower() or 
                keyword_lower in faq['answer'].lower()):
                results.append(faq)
        return results
