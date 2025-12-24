"""
Safety Guard Module - Input and Output Filtering
Prevents prompt injection and filters sensitive content
"""

import re
from typing import Tuple, List
from config import Config


class SafetyGuard:
    def __init__(self):
        self.sensitive_words = self._load_sensitive_words()
        self.prompt_injection_patterns = [
            r'ignore\s+(previous|above|all)\s+instructions',
            r'you\s+are\s+now',
            r'forget\s+everything',
            r'new\s+instructions',
            r'system\s*:\s*',
            r'<\|.*?\|>',  # Special tokens
        ]
    
    def _load_sensitive_words(self) -> List[str]:
        """Load sensitive words from file"""
        try:
            with open(Config.SENSITIVE_WORDS_FILE, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f if line.strip()]
                return words
        except FileNotFoundError:
            # Default sensitive words if file not found
            return ['password', 'credit card', 'ssn', 'secret']
    
    def check_input(self, text: str) -> Tuple[bool, str]:
        """
        Check if input is safe
        Returns: (is_safe, message)
        """
        # Check length
        if len(text) > Config.MAX_INPUT_LENGTH:
            return False, "Input too long"
        
        # Check for prompt injection
        text_lower = text.lower()
        for pattern in self.prompt_injection_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return False, "Potential prompt injection detected"
        
        # Check for sensitive words in input (for logging purposes)
        for word in self.sensitive_words:
            if word.lower() in text_lower:
                # Don't block, just warn
                return True, f"Warning: sensitive word '{word}' detected in input"
        
        return True, "Input is safe"
    
    def filter_output(self, text: str) -> Tuple[str, bool]:
        """
        Filter output for sensitive content
        Returns: (filtered_text, was_filtered)
        """
        original_text = text
        was_filtered = False
        
        # Remove sensitive words from output
        for word in self.sensitive_words:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            if pattern.search(text):
                text = pattern.sub('[FILTERED]', text)
                was_filtered = True
        
        # Check for potential data leakage patterns
        # Email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.search(email_pattern, text):
            text = re.sub(email_pattern, '[EMAIL]', text)
            was_filtered = True
        
        # Phone numbers (simple pattern)
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        if re.search(phone_pattern, text):
            text = re.sub(phone_pattern, '[PHONE]', text)
            was_filtered = True
        
        return text, was_filtered
    
    def sanitize_input(self, text: str) -> str:
        """Remove potentially harmful characters"""
        # Remove null bytes
        text = text.replace('\x00', '')
        # Normalize whitespace
        text = ' '.join(text.split())
        return text.strip()
