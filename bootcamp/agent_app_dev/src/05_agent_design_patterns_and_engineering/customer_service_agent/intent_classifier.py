"""
Intent Classifier Module
Classifies user intent: FAQ, General Question, or Chitchat
"""

from typing import Tuple
from config import Config


class IntentClassifier:
    def __init__(self):
        # Keywords for different intents
        self.faq_keywords = [
            'how to', 'how do', 'what is', 'when', 'where',
            'price', 'cost', 'payment', 'shipping', 'return',
            'account', 'password', 'login', 'register',
            'hours', 'contact', 'support', 'help'
        ]
        
        self.chitchat_keywords = [
            'hello', 'hi', 'hey', 'good morning', 'good afternoon',
            'how are you', 'thanks', 'thank you', 'bye', 'goodbye',
            'nice', 'great', 'awesome', 'cool'
        ]
    
    def classify(self, text: str) -> Tuple[str, float]:
        """
        Classify user intent
        Returns: (intent_type, confidence)
        Intent types: 'faq', 'general', 'chitchat'
        """
        text_lower = text.lower()
        
        # Check for chitchat
        chitchat_matches = sum(
            1 for keyword in self.chitchat_keywords 
            if keyword in text_lower
        )
        if chitchat_matches > 0 and len(text.split()) <= 10:
            confidence = min(0.9, 0.6 + chitchat_matches * 0.1)
            return 'chitchat', confidence
        
        # Check for FAQ patterns
        faq_matches = sum(
            1 for keyword in self.faq_keywords 
            if keyword in text_lower
        )
        
        # Question marks often indicate questions
        has_question_mark = '?' in text
        
        if faq_matches > 0 or has_question_mark:
            confidence = min(0.95, Config.FAQ_CONFIDENCE_THRESHOLD + faq_matches * 0.1)
            return 'faq', confidence
        
        # Default to general question
        return 'general', 0.5
    
    def should_use_rag(self, intent: str, confidence: float) -> bool:
        """Determine if RAG retrieval should be used"""
        if intent == 'chitchat':
            return False
        if intent == 'faq' and confidence >= Config.FAQ_CONFIDENCE_THRESHOLD:
            return True
        if intent == 'general':
            return True
        return True
