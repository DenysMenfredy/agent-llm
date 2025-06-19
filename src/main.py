from llm import OllamaLLM
from agent import ResearchAgent


def main():
    """Example usage of the Research Agent"""
    
    print("🤖 Research Agent - Powered by Open Source LLM")
    print("=" * 50)
    
    # Initialize the LLM (make sure Ollama is running)
    llm = OllamaLLM(model="llama3.2")  # You can change this to any model you have
    
    # Create the agent
    agent = ResearchAgent(llm)
    
    # Example research tasks
    example_tasks = [
        "Research the current state of renewable energy adoption globally",
        "What are the main challenges in artificial intelligence ethics?",
        "Explain the recent developments in quantum computing",
    ]
    
    print("Example tasks:")
    for i, task in enumerate(example_tasks, 1):
        print(f"{i}. {task}")
    
    print("\nOr enter your own research topic!")
    
    # Get user input
    choice = input("\nEnter task number (1-3) or type your own research topic: ").strip()
    
    if choice in ["1", "2", "3"]:
        task = example_tasks[int(choice) - 1]
    else:
        task = choice
    
    # Run the research
    try:
        result = agent.run(task)
        print("\n" + "="*50)
        print("📋 RESEARCH REPORT")
        print("="*50)
        print(result)
    except KeyboardInterrupt:
        print("\n\nResearch interrupted by user.")
    except Exception as e:
        print(f"\nError during research: {e}")

if __name__ == "__main__":
    main()