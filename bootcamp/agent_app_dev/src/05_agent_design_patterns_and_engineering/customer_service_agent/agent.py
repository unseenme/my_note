"""
Main Customer Service Agent
Orchestrates all modules to handle user queries
"""

import httpx
from typing import Dict, List, Optional
from config import Config
from safety_guard import SafetyGuard
from intent_classifier import IntentClassifier
from knowledge_base import KnowledgeBase
from rag_retriever import RAGRetriever
from validator_agent import ValidatorAgent
from observer import Observer


class CustomerServiceAgent:
    def __init__(self):
        print("Initializing Customer Service Agent...")
        
        # Initialize all modules
        self.safety_guard = SafetyGuard()
        self.intent_classifier = IntentClassifier()
        self.knowledge_base = KnowledgeBase()
        self.rag_retriever = RAGRetriever(self.knowledge_base)
        self.validator = ValidatorAgent()
        self.observer = Observer()
        
        # Conversation history
        self.conversation_history: List[Dict] = []
        
        print("Agent initialized successfully!")
    
    def _call_llm(self, messages: list, temperature: float = None) -> tuple:
        """
        Call LLM API
        Returns: (response_text, input_tokens, output_tokens)
        """
        if temperature is None:
            temperature = Config.LLM_TEMPERATURE
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Config.LLM_API_KEY}"
        }
        
        payload = {
            "model": Config.LLM_MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": Config.LLM_MAX_TOKENS
        }
        
        try:
            response = httpx.post(
                Config.LLM_API_URL,
                json=payload,
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()
            result = response.json()
            
            content = result['choices'][0]['message']['content']
            usage = result.get('usage', {})
            input_tokens = usage.get('prompt_tokens', 0)
            output_tokens = usage.get('completion_tokens', 0)
            
            # Track in observer
            self.observer.track_llm_call(Config.LLM_MODEL, input_tokens, output_tokens)
            
            return content, input_tokens, output_tokens
            
        except Exception as e:
            print(f"LLM API Error: {e}")
            return f"I apologize, but I'm experiencing technical difficulties. Please try again later.", 0, 0
    
    def _generate_response(self, query: str, intent: str, 
                          context: str, sources: List[str]) -> str:
        """Generate response using LLM"""
        
        # Build system prompt based on intent
        if intent == 'chitchat':
            system_prompt = "You are a friendly customer service assistant. Respond warmly to greetings and casual conversation."
        else:
            system_prompt = """You are a helpful customer service assistant. 
Use the provided knowledge base to answer questions accurately.
Always cite your sources using [Source: FAQ-X] format.
If information is not in the knowledge base, clearly state that you don't have that information.
Be concise and helpful."""
        
        # Build user prompt
        if intent == 'chitchat':
            user_prompt = query
        else:
            user_prompt = f"""User Query: {query}

{context}

Please answer the user's query based on the knowledge base provided above.
Remember to cite sources and be honest about limitations."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Add conversation history (last 3 turns)
        if self.conversation_history:
            history_context = "\n\nRecent conversation history:\n"
            for turn in self.conversation_history[-3:]:
                history_context += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"
            messages[1]['content'] = history_context + "\n" + messages[1]['content']
        
        response, _, _ = self._call_llm(messages)
        return response
    
    def process_query(self, query: str) -> Dict:
        """
        Main method to process user query
        Returns response dictionary with answer and metadata
        """
        print(f"\n{'='*60}")
        print(f"Processing Query: {query}")
        print(f"{'='*60}")
        
        # Step 1: Safety Guard - Input Check
        input_safe, safety_message = self.safety_guard.check_input(query)
        if not input_safe:
            self.observer.log_safety_check(False, False, safety_message)
            return {
                'answer': "I cannot process this request due to safety concerns.",
                'sources': [],
                'validation_passed': False,
                'metadata': {'safety_blocked': True}
            }
        
        # Sanitize input
        query = self.safety_guard.sanitize_input(query)
        
        # Step 2: Intent Classification
        intent, confidence = self.intent_classifier.classify(query)
        print(f"Intent: {intent} (confidence: {confidence:.2f})")
        self.observer.log_intent_classification(query, intent, confidence)
        
        # Step 3: RAG Retrieval (if needed)
        context = ""
        sources = []
        retrieved_items = []
        
        if self.intent_classifier.should_use_rag(intent, confidence):
            retrieved_items = self.rag_retriever.retrieve(query)
            if retrieved_items:
                context = self.rag_retriever.format_context(retrieved_items)
                sources = self.rag_retriever.get_sources(retrieved_items)
                print(f"Retrieved {len(retrieved_items)} relevant FAQs")
                self.observer.log_rag_retrieval(query, len(retrieved_items), sources)
            else:
                print("No relevant FAQs found")
        
        # Step 4: Generate Response
        response = self._generate_response(query, intent, context, sources)
        print(f"\nGenerated Response: {response[:100]}...")
        
        # Step 5: Validate Response (if not chitchat)
        validation_passed = True
        validation_feedback = ""
        
        if intent != 'chitchat' and context:
            print("\nValidating response...")
            validation_passed, validation_feedback, _ = self.validator.validate_response(
                query, response, context, sources
            )
            print(f"Validation: {'PASSED' if validation_passed else 'FAILED'}")
            
            # If validation failed, try to improve
            if not validation_passed:
                print("Attempting to improve response...")
                response = self.validator.suggest_improvement(
                    query, response, validation_feedback
                )
        
        # Step 6: Safety Guard - Output Filter
        response, was_filtered = self.safety_guard.filter_output(response)
        self.observer.log_safety_check(True, was_filtered, "Output check completed")
        
        # Step 7: Log Response
        self.observer.log_response(query, response, sources, validation_passed)
        
        # Update conversation history
        self.conversation_history.append({
            'user': query,
            'assistant': response
        })
        
        # Return result
        return {
            'answer': response,
            'sources': sources,
            'intent': intent,
            'confidence': confidence,
            'validation_passed': validation_passed,
            'validation_feedback': validation_feedback if not validation_passed else None,
            'metadata': {
                'num_retrieved': len(retrieved_items),
                'output_filtered': was_filtered
            }
        }
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        print("Conversation history reset.")
    
    def get_session_summary(self):
        """Get session summary from observer"""
        return self.observer.get_session_summary()
    
    def print_session_summary(self):
        """Print session summary"""
        self.observer.print_summary()
