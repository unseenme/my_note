"""
Observer Module - Logging and Monitoring
Implements observability for the agent system
"""

import json
import os
from datetime import datetime
from typing import Dict, Any
from config import Config


class Observer:
    def __init__(self):
        self.session_logs = []
        self.total_cost = 0.0
        self.total_tokens = {'input': 0, 'output': 0}
        self._ensure_log_dir()
    
    def _ensure_log_dir(self):
        """Ensure log directory exists"""
        log_dir = os.path.dirname(Config.LOG_FILE)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    def log_interaction(self, event_type: str, data: Dict[str, Any]):
        """Log an interaction event"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data
        }
        self.session_logs.append(log_entry)
        
        # Write to file
        self._write_to_file(log_entry)
    
    def _write_to_file(self, log_entry: Dict):
        """Write log entry to file"""
        try:
            with open(Config.LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Warning: Could not write to log file: {e}")
    
    def track_llm_call(self, model: str, input_tokens: int, output_tokens: int):
        """Track LLM API call and cost"""
        self.total_tokens['input'] += input_tokens
        self.total_tokens['output'] += output_tokens
        
        if Config.ENABLE_COST_TRACKING:
            cost = (
                (input_tokens / 1000) * Config.COST_PER_1K_INPUT_TOKENS +
                (output_tokens / 1000) * Config.COST_PER_1K_OUTPUT_TOKENS
            )
            self.total_cost += cost
            
            self.log_interaction('llm_call', {
                'model': model,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'cost': cost
            })
    
    def log_safety_check(self, input_safe: bool, output_filtered: bool, messages: str):
        """Log safety guard results"""
        self.log_interaction('safety_check', {
            'input_safe': input_safe,
            'output_filtered': output_filtered,
            'messages': messages
        })
    
    def log_intent_classification(self, query: str, intent: str, confidence: float):
        """Log intent classification results"""
        self.log_interaction('intent_classification', {
            'query': query,
            'intent': intent,
            'confidence': confidence
        })
    
    def log_rag_retrieval(self, query: str, num_results: int, sources: list):
        """Log RAG retrieval results"""
        self.log_interaction('rag_retrieval', {
            'query': query,
            'num_results': num_results,
            'sources': sources
        })
    
    def log_response(self, query: str, response: str, sources: list, 
                    validation_passed: bool):
        """Log final response"""
        self.log_interaction('response', {
            'query': query,
            'response': response[:200] + '...' if len(response) > 200 else response,
            'sources': sources,
            'validation_passed': validation_passed
        })
    
    def get_session_summary(self) -> Dict:
        """Get summary of current session"""
        return {
            'total_interactions': len(self.session_logs),
            'total_cost': round(self.total_cost, 4),
            'total_tokens': self.total_tokens,
            'session_start': self.session_logs[0]['timestamp'] if self.session_logs else None,
            'session_end': self.session_logs[-1]['timestamp'] if self.session_logs else None
        }
    
    def print_summary(self):
        """Print session summary to console"""
        summary = self.get_session_summary()
        print("\n" + "="*50)
        print("SESSION SUMMARY")
        print("="*50)
        print(f"Total Interactions: {summary['total_interactions']}")
        print(f"Total Cost: ${summary['total_cost']:.4f}")
        print(f"Input Tokens: {summary['total_tokens']['input']}")
        print(f"Output Tokens: {summary['total_tokens']['output']}")
        print("="*50 + "\n")
