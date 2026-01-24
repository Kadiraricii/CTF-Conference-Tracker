import logging

logger = logging.getLogger(__name__)

class AIService:
    # Basic Keywords for Heuristic "AI"
    KEYWORDS = {
        "web": ["xss", "csrf", "injection", "web", "frontend", "http"],
        "crypto": ["crypto", "cryptography", "rsa", "aes", "encryption"],
        "pwn": ["pwn", "overflow", "rop", "heap", "binary", "exploit"],
        "forensics": ["forensics", "stegano", "pcap", "network analysis"],
        "cloud": ["aws", "azure", "gcp", "cloud", "kubernetes", "docker"],
        "ml": ["machine learning", "adversarial", "ai", "model"]
    }

    @classmethod
    async def generate_tags(cls, title: str, description: str) -> list:
        """
        Generate tags for an event based on its content.
        TODO: Integrate OpenAI/Gemini API here for advanced tagging.
        """
        text = (title + " " + description).lower()
        tags = set()

        # 1. Heuristic Check
        for category, words in cls.KEYWORDS.items():
            if any(word in text for word in words):
                tags.add(category)

        # 2. LLM Placeholder (If Key exists)
        # if settings.OPENAI_API_KEY:
        #    tags.update(await cls.call_llm(text))
        
        return list(tags)
