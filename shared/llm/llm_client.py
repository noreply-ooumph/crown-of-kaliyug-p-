"""
Crown of Kaliyug — LLM Client
Phase 1 · shared/llm/llm_client.py

Primary:  Groq API + Llama 3.3 70B  (dev / MVP)
Fallback: Claude Sonnet 4.6          (production — swap LLM_PROVIDER=claude)

To switch to Claude: set LLM_PROVIDER=claude in .env
"""
import os
import json
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()



# ── GROQ CLIENT ───────────────────────────────────────────────────────────────
if LLM_PROVIDER == "groq":
    from groq import Groq
    _groq = Groq(api_key=os.getenv("GROQ_API_KEY", ""))
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# ── CLAUDE CLIENT ─────────────────────────────────────────────────────────────
elif LLM_PROVIDER == "claude":
    import anthropic
    _claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")


@retry(stop=stop_after_attempt(5), wait=wait_exponential(min=4, max=30))
def call_llm(
    system_prompt: str,
    user_message:  str,
    max_tokens:    int   = 8192,
    json_mode:     bool  = False,
    temperature:   float = 0.7,
) -> str:
    """
    Single entry point for all LLM calls across Phase 1 agents.
    Swap LLM_PROVIDER env var to switch between Groq and Claude.
    """
    if json_mode:
        user_message += (
            "\n\nIMPORTANT: Respond ONLY with valid JSON. "
            "No preamble, no markdown fences, no explanation."
        )

    if LLM_PROVIDER == "groq":
        return _call_groq(system_prompt, user_message, max_tokens, temperature)
    elif LLM_PROVIDER == "claude":
        return _call_claude(system_prompt, user_message, max_tokens)
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {LLM_PROVIDER}")


def call_llm_json(
    system_prompt: str,
    user_message:  str,
    max_tokens:    int = 8192,
) -> dict:
    """Calls LLM and returns parsed JSON dict. Strips markdown fences if present."""
    raw = call_llm(
        system_prompt=system_prompt,
        user_message=user_message,
        max_tokens=max_tokens,
        json_mode=True,
    )
    clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse failed: {e}\nRaw output:\n{clean[:500]}")
        raise


def _call_groq(system_prompt: str, user_message: str,
               max_tokens: int, temperature: float) -> str:
    response = _groq.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system",  "content": system_prompt},
            {"role": "user",    "content": user_message},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    text = response.choices[0].message.content
    logger.debug(f"[Groq] {GROQ_MODEL} - "
                 f"{response.usage.prompt_tokens} in / {response.usage.completion_tokens} out")
    return text


def _call_claude(system_prompt: str, user_message: str, max_tokens: int) -> str:
    response = _claude.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    text = response.content[0].text
    logger.debug(f"[Claude] {CLAUDE_MODEL} - "
                 f"{response.usage.input_tokens} in / {response.usage.output_tokens} out")
    return text


def load_story_bible_prompt(character_id: str = None) -> str:
    """Loads world rules + optional character profile as system prompt context."""
    parts = []
    try:
        with open("story_bible/world_rules.md", "r", encoding="utf-8") as f:
            parts.append(f"## WORLD RULES\n{f.read()}")
    except FileNotFoundError:
        logger.warning("world_rules.md not found")

    if character_id:
        try:
            with open(f"story_bible/characters/{character_id}.md", "r", encoding="utf-8") as f:
                parts.append(f"## CHARACTER: {character_id.upper()}\n{f.read()}")

        except FileNotFoundError:
            logger.warning(f"Character file not found: {character_id}.md")

    return "\n\n---\n\n".join(parts)