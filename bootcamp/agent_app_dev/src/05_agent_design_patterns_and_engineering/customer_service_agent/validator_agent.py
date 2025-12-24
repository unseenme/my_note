"""
Validator Agent Module
Second agent to validate and challenge the first agent's response
This helps reduce AI hallucination (课程中的"白脸"角色)
"""

import json
import httpx
from typing import Dict, Tuple
from config import Config


class ValidatorAgent:
    def __init__(self):
        self.api_url = Config.LLM_API_URL
        self.api_key = Config.LLM_API_KEY
        self.model = Config.LLM_MODEL
    
    def _call_llm(self, messages: list) -> str:
        """Call LLM API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": Config.VALIDATOR_TEMPERATURE,
            "max_tokens": 500
        }
        
        try:
            response = httpx.post(
                self.api_url, 
                json=payload, 
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"Validator LLM call error: {e}")
            return ""
    
    def validate_response(self, query: str, response: str, 
                         context: str, sources: list) -> Tuple[bool, str, Dict]:
        """
        Validate if the response is accurate and grounded in context
        Returns: (is_valid, feedback, validation_details)
        """
        validation_prompt = f"""You are a strict validator agent. Your job is to check if the answer is accurate and grounded in the provided knowledge base.

User Query: {query}

Knowledge Base Context:
{context}

Proposed Answer:
{response}

Sources Referenced: {', '.join(sources) if sources else 'None'}

Please validate the answer by checking:
1. Is the answer grounded in the provided knowledge base?
2. Does it contain any information not supported by the sources?
3. Is the answer accurate and not hallucinated?
4. Does it properly address the user's query?

Respond in JSON format:
{{
    "is_valid": true/false,
    "confidence": 0.0-1.0,
    "issues": ["list of issues found, if any"],
    "feedback": "brief explanation"
}}
"""
        
        messages = [
            {"role": "system", "content": "You are a validation agent that checks answer accuracy."},
            {"role": "user", "content": validation_prompt}
        ]
        
        validation_result = self._call_llm(messages)
        
        try:
            # Parse JSON response
            validation_data = json.loads(validation_result)
            is_valid = validation_data.get('is_valid', True)
            feedback = validation_data.get('feedback', '')
            
            return is_valid, feedback, validation_data
        except json.JSONDecodeError:
            # If JSON parsing fails, do basic validation
            is_valid = 'false' not in validation_result.lower()
            return is_valid, validation_result, {'is_valid': is_valid}
    
    def suggest_improvement(self, query: str, original_response: str, 
                           validation_feedback: str) -> str:
        """Suggest improved response based on validation feedback"""
        improvement_prompt = f"""The following answer was found to have issues:

Original Answer: {original_response}

Validation Feedback: {validation_feedback}

User Query: {query}

Please provide an improved answer that addresses the validation issues. If you cannot provide accurate information, clearly state the limitations.
"""
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant that provides accurate information."},
            {"role": "user", "content": improvement_prompt}
        ]
        
        improved_response = self._call_llm(messages)
        return improved_response
