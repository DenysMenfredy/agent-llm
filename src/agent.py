import re
from typing import List, Optional
import requests
from llm import OllamaLLM
from tools import WebSearchTool, SummaryTool
from utils import Message

class ResearchAgent:
    """A research agent that can search the web and compile comprehensive reports"""
    
    def __init__(self, llm: OllamaLLM):
        self.llm = llm
        self.tools = {
            "web_search": WebSearchTool(),
            "summarize": SummaryTool()
        }
        self.conversation_history: List[Message] = []
        self.max_iterations = 5
    
    def run(self, task: str) -> str:
        """Main agent loop"""
        print(f"🔍 Starting research on: {task}")
        
        # Initialize conversation with system prompt
        system_prompt = self._get_system_prompt()
        self.conversation_history = [Message("system", system_prompt)]
        
        # Add user task
        self.conversation_history.append(Message("user", task))
        
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # Get agent's response
            response = self.llm.generate(self.conversation_history)
            print(f"Agent thinking: {response[:200]}...")
            
            # Check if agent wants to use a tool
            tool_call = self._extract_tool_call(response)
            
            if tool_call:
                tool_name, tool_args = tool_call
                print(f"🔧 Using tool: {tool_name}")
                
                # Execute tool
                if tool_name in self.tools:
                    tool_result = self.tools[tool_name].execute(**tool_args)
                    print(f"📊 Tool result: {tool_result[:100]}...")
                    
                    # Add tool result to conversation
                    self.conversation_history.append(Message("assistant", response))
                    self.conversation_history.append(Message("user", f"Tool result: {tool_result}"))
                else:
                    self.conversation_history.append(Message("assistant", f"Error: Unknown tool '{tool_name}'"))
            
            elif "FINAL_ANSWER:" in response:
                # Agent has completed the task
                final_answer = response.split("FINAL_ANSWER:")[-1].strip()
                print(f"\n✅ Research completed!")
                return final_answer
            
            else:
                # Agent is just thinking, continue
                self.conversation_history.append(Message("assistant", response))
        
        return "Research completed but agent didn't provide a final answer within the iteration limit."
    
    def _get_system_prompt(self) -> str:
        tools_desc = "\n".join([f"- {tool.description()}" for tool in self.tools.values()])
        
        return f"""You are a research agent. Your job is to help users research topics by gathering information and providing comprehensive reports.

Available tools:
{tools_desc}

To use a tool, write: TOOL_CALL: tool_name(arg1="value1", arg2="value2")

Your research process should be:
1. Break down the research topic into key questions
2. Use web_search to find information about different aspects
3. Use summarize to organize the information you find
4. Provide a comprehensive final answer

When you're ready to give your final answer, write: FINAL_ANSWER: [your comprehensive response]

Be thorough, accurate, and cite your sources when possible."""
    
    def _extract_tool_call(self, response: str) -> Optional[tuple]:
        """Extract tool calls from agent response"""
        if "TOOL_CALL:" not in response:
            return None
        
        try:
            # Find the tool call line
            lines = response.split('\n')
            tool_line = None
            for line in lines:
                if "TOOL_CALL:" in line:
                    tool_line = line.split("TOOL_CALL:")[-1].strip()
                    break
            
            if not tool_line:
                return None
            
            # Parse tool call: tool_name(arg1="value1", arg2="value2")
            match = re.match(r'(\w+)\((.*)\)', tool_line)
            if not match:
                return None
            
            tool_name = match.group(1)
            args_str = match.group(2)
            
            # Simple argument parsing
            args = {}
            if args_str:
                # Handle simple cases like query="search term"
                arg_matches = re.findall(r'(\w+)="([^"]*)"', args_str)
                for key, value in arg_matches:
                    args[key] = value
            
            return tool_name, args
            
        except Exception as e:
            print(f"Error parsing tool call: {e}")
            return None

def diagnose_ollama():
    """Diagnose common Ollama issues"""
    print("🔍 Diagnosing Ollama setup...")
    
    try:
        # Check if Ollama is running
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama is running")
            print(f"📦 Available models: {[m['name'] for m in models]}")
            
            if not models:
                print("❌ No models installed!")
                print("Run: ollama pull llama3.2")
                return False
            return True
        else:
            print(f"❌ Ollama responded with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama")
        print("Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
