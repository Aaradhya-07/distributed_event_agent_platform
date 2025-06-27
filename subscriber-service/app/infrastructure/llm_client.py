import httpx
from shared.config import Settings

class GroqLLMClient:
    """Client for interacting with the Groq LLM API for property extraction."""
    def __init__(self, settings: Settings):
        """Initialize the LLM client with API settings."""
        self.api_url = settings.llm_api_url
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model

    async def extract_properties(self, molecule_data):
        """Call the LLM API to extract chemical properties from molecule data.
        Args:
            molecule_data: Dictionary of molecule information.
        Returns:
            The LLM API response as a dictionary.
        Raises:
            Exception if the API call fails or is rate limited.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        prompt = f"Extract the chemical properties (color, pH, etc.) from the following molecule data: {molecule_data}"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a chemistry assistant. Extract properties from molecule data."},
                {"role": "user", "content": prompt}
            ]
        }
        async with httpx.AsyncClient(timeout=10) as client:
            try:
                response = await client.post(self.api_url, json=payload, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    raise Exception("LLM rate limit exceeded")
                raise
            except Exception as e:
                raise Exception(f"LLM API error: {e}") 