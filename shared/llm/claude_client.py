"""
Crown of Kaliyug — Claude API Client
Phase 0: Foundation
"""
import os
import anthropic
from typing import Optional, Dict, Any
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

class ClaudeClient:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            logger.warning("ANTHROPIC_API_KEY not found in environment.")
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20240620"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def generate(self, system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
        try:
            # Add JSON instructions if needed
            if json_mode:
                user_prompt += "\n\nReturn ONLY a valid JSON object."

            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                # Anthropic prompt caching (beta) - useful for Story Bible
                extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"}
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude API Error: {str(e)}")
            raise

claude = ClaudeClient()

def call_claude(system_prompt: str, user_message: str, max_tokens: int = 4000) -> str:
    """Wrapper function for test compatibility."""
    return claude.generate(system_prompt, user_message)
