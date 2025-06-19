from abc import ABC, abstractmethod
import re
import requests

class Tool(ABC):
    @abstractmethod
    def execute(self, **kwargs)->str:
        pass

    @abstractmethod
    def description(self)->str:
        pass


class SummaryTool(Tool):
    """Tool to help organize and summarize information."""

    def execute(self, text: str, focus: str = "general")->str:
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in  sentences if len(s.strip()) > 20]

        summary_parts = []
        if sentences:
            summary_parts.append("Key Points")
            summary_parts.extend([f"- {s}." for s in sentences[:3]])

        return "\n".join(summary_parts) if summary_parts else "No content to summarize."

    def description(self)->str:
        return "summarize(text: str, focus: str = 'general') - Summarize and organize text information."


class WebSearchTool(Tool):
    """Simple web search tool using DuckDuckGo Instant Answer API"""
    
    def execute(self, query: str) -> str:
        try:
            # Using DuckDuckGo Instant Answer API (free, no API key needed)
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            # Extract relevant information
            result = []
            if data.get('Abstract'):
                result.append(f"Summary: {data['Abstract']}")
            
            if data.get('RelatedTopics'):
                result.append("Related Information:")
                for topic in data['RelatedTopics'][:3]:  # Limit to first 3
                    if isinstance(topic, dict) and 'Text' in topic:
                        result.append(f"- {topic['Text']}")
            
            return "\n".join(result) if result else f"No detailed information found for '{query}'. Try a more specific search term."
            
        except Exception as e:
            return f"Search failed: {str(e)}"
    
    def description(self) -> str:
        return "web_search(query: str) - Search the web for information about a topic"