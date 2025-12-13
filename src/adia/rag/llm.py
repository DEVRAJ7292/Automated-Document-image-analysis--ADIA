import google.generativeai as genai

from adia.core.config import get_settings


class LLMClient:
    """
    Gemini-only LLM client.
    """

    def __init__(self):
        settings = get_settings()

        if not settings.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is not set")

        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 512,
            },
        )
        return response.text.strip()
