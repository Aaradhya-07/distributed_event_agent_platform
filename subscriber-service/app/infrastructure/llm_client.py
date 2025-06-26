import httpx
from shared.config import Settings

class GroqLLMClient:
    def __init__(self, settings: Settings):
        self.api_url = settings.llm_api_url
        self.api_key = settings.llm_api_key

    async def extract_properties(self, molecule_data):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "molecule_data": molecule_data
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