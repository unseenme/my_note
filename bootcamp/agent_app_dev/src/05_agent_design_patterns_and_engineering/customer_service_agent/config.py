"""
Configuration file for Customer Service Agent
"""

class Config:
    # LLM API Configuration (Using DeepSeek as example, can be changed to OpenAI/Claude)
    LLM_API_URL = "https://api.deepseek.com/v1/chat/completions"
    LLM_API_KEY = "your-api-key-here"  # Replace with your actual API key
    LLM_MODEL = "deepseek-chat"
    LLM_TEMPERATURE = 0.7
    LLM_MAX_TOKENS = 1000
    
    # For validator agent, use lower temperature for more accurate validation
    VALIDATOR_TEMPERATURE = 0.3
    
    # RAG Configuration
    RAG_TOP_K = 3  # Number of knowledge base items to retrieve
    RAG_SIMILARITY_THRESHOLD = 0.6  # Minimum similarity score
    
    # Safety Guard Configuration
    SENSITIVE_WORDS_FILE = "data/sensitive_words.txt"
    MAX_INPUT_LENGTH = 1000
    
    # Intent Classification Thresholds
    FAQ_CONFIDENCE_THRESHOLD = 0.7
    
    # Observer Configuration
    LOG_FILE = "logs/agent.log"
    ENABLE_COST_TRACKING = True
    
    # Token cost (adjust based on your LLM provider)
    COST_PER_1K_INPUT_TOKENS = 0.0014  # DeepSeek pricing
    COST_PER_1K_OUTPUT_TOKENS = 0.0028
