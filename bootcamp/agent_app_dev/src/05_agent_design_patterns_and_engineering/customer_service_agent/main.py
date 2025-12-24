"""
Main Demo Application
Run this to test the Customer Service Agent
"""

import os
from agent import CustomerServiceAgent


def print_response(result: dict):
    """Pretty print agent response"""
    print("\n" + "="*60)
    print("AGENT RESPONSE")
    print("="*60)
    print(f"\nAnswer:\n{result['answer']}\n")
    
    if result.get('sources'):
        print(f"Sources: {', '.join(result['sources'])}")
    
    print(f"\nIntent: {result.get('intent')} (confidence: {result.get('confidence', 0):.2f})")
    print(f"Validation: {'✓ PASSED' if result.get('validation_passed') else '✗ FAILED'}")
    
    if result.get('validation_feedback'):
        print(f"Validation Feedback: {result['validation_feedback']}")
    
    print("\nMetadata:")
    for key, value in result.get('metadata', {}).items():
        print(f"  {key}: {value}")
    print("="*60 + "\n")


def create_sample_data():
    """Create sample data files if they don't exist"""
    # Create data directory
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Create sensitive words file
    if not os.path.exists('data/sensitive_words.txt'):
        with open('data/sensitive_words.txt', 'w', encoding='utf-8') as f:
            f.write("password\n")
            f.write("credit card\n")
            f.write("ssn\n")
            f.write("secret key\n")
        print("✓ Created data/sensitive_words.txt")


def demo_mode():
    """Run demo with predefined queries"""
    print("\n" + "="*60)
    print("CUSTOMER SERVICE AGENT - DEMO MODE")
    print("="*60)
    
    # Create sample data
    create_sample_data()
    
    # Initialize agent
    agent = CustomerServiceAgent()
    
    # Demo queries
    demo_queries = [
        "Hello! How are you?",
        "What are your business hours?",
        "How do I reset my password?",
        "What payment methods do you accept?",
        "Do you ship to Mars?",  # Not in knowledge base
    ]
    
    for query in demo_queries:
        result = agent.process_query(query)
        print_response(result)
        input("Press Enter to continue...")
    
    # Print session summary
    agent.print_session_summary()


def interactive_mode():
    """Run in interactive mode"""
    print("\n" + "="*60)
    print("CUSTOMER SERVICE AGENT - INTERACTIVE MODE")
    print("="*60)
    print("\nCommands:")
    print("  'quit' or 'exit' - Exit the program")
    print("  'reset' - Reset conversation history")
    print("  'summary' - Show session summary")
    print("="*60 + "\n")
    
    # Create sample data
    create_sample_data()
    
    # Initialize agent
    agent = CustomerServiceAgent()
    
    while True:
        try:
            query = input("\nYou: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit']:
                print("\nThank you for using Customer Service Agent!")
                agent.print_session_summary()
                break
            
            if query.lower() == 'reset':
                agent.reset_conversation()
                continue
            
            if query.lower() == 'summary':
                agent.print_session_summary()
                continue
            
            # Process query
            result = agent.process_query(query)
            print(f"\nAgent: {result['answer']}")
            
            if result.get('sources'):
                print(f"\n[Sources: {', '.join(result['sources'])}]")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
            agent.print_session_summary()
            break
        except Exception as e:
            print(f"\nError: {e}")


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("CUSTOMER SERVICE AGENT")
    print("Agent Design Pattern & Engineering Practice")
    print("="*60)
    
    # Check if API key is configured
    from config import Config
    if Config.LLM_API_KEY == "your-api-key-here":
        print("\n⚠️  WARNING: Please configure your LLM API key in config.py")
        print("   Set Config.LLM_API_KEY to your actual API key")
        print("\n   For testing without API, you can modify the code to use")
        print("   mock responses or run with limited functionality.\n")
    
    print("\nSelect mode:")
    print("1. Demo Mode (predefined queries)")
    print("2. Interactive Mode (chat with agent)")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        demo_mode()
    elif choice == '2':
        interactive_mode()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
