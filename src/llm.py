from typing import List
import requests
from utils import Message

class OllamaLLM:
    """Interface to Ollama for local LLM inference"""
    
    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self._check_model_availability()
    
    def _check_model_availability(self):
        """Check if the model is available and suggest alternatives if not"""
        try:
            # List available models
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get("models", [])
                available_models = [model["name"] for model in models]
                
                if not any(self.model in model for model in available_models):
                    print(f"⚠️  Model '{self.model}' not found!")
                    print(f"Available models: {available_models}")
                    if available_models:
                        suggested_model = available_models[0]
                        print(f"Using '{suggested_model}' instead...")
                        self.model = suggested_model
                    else:
                        print("No models available. Please install one with: ollama pull llama3.2")
                else:
                    print(f"✅ Using model: {self.model}")
        except Exception as e:
            print(f"Warning: Could not check model availability: {e}")
    
    def generate(self, messages: List[Message], max_tokens: int = 1000) -> str:
        try:
            # Use chat API instead of generate for better compatibility
            ollama_messages = []
            for msg in messages:
                if msg.role == "system":
                    ollama_messages.append({"role": "system", "content": msg.content})
                elif msg.role == "user":
                    ollama_messages.append({"role": "user", "content": msg.content})
                elif msg.role == "assistant":
                    ollama_messages.append({"role": "assistant", "content": msg.content})
            
            payload = {
                "model": self.model,
                "messages": ollama_messages,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.3,  # Lower temperature for more consistent tool calling
                    "top_p": 0.9,
                    "stop": ["Human:", "User:"]  # Stop tokens to prevent runaway generation
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=120  # Increased timeout for longer responses
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["message"]["content"]
            else:
                error_details = ""
                try:
                    error_info = response.json()
                    error_details = f" - {error_info.get('error', 'Unknown error')}"
                except:
                    pass
                return f"Error: HTTP {response.status_code}{error_details}. Try: 1) Check if model exists with 'ollama list', 2) Pull model with 'ollama pull {self.model}'"
                
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Make sure Ollama is running with: 'ollama serve'"
        except requests.exceptions.Timeout:
            return "Error: Request timed out. The model might be too large or the prompt too complex."
        except Exception as e:
            return f"Error generating response: {str(e)}"