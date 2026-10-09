"""Single entry point for LLM calls. Only uses models allowed by WTQ 2026.

Set LLM_PROVIDER in .env to one of: gemini | anthropic | openai
Set LLM_MODEL to the exact model ID from the WTQ PDF.
"""
import json
import os
import re
import time

from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

DEFAULT_MODELS = {
    "gemini": "gemini-3.1-flashlite",
    "anthropic": "claude-haiku-4-5",
    "openai": "gpt-4.1-mini",
}
MODEL = os.getenv("LLM_MODEL", DEFAULT_MODELS[PROVIDER])


def _call_gemini(prompt: str, system: str, temperature: float) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    resp = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system or None, temperature=temperature
        ),
    )
    return resp.text


def _call_anthropic(prompt: str, system: str, temperature: float) -> str:
    import anthropic

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    resp = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        temperature=temperature,
        system=system or "You are a helpful assistant.",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def _call_openai(prompt: str, system: str, temperature: float) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    kwargs = {"model": MODEL, "messages": messages}
    # gpt-5-mini only supports the default temperature
    if not MODEL.startswith("gpt-5"):
        kwargs["temperature"] = temperature
    resp = client.chat.completions.create(**kwargs)
    return resp.choices[0].message.content


_PROVIDERS = {
    "gemini": _call_gemini,
    "anthropic": _call_anthropic,
    "openai": _call_openai,
}


def call_llm(prompt: str, system: str = "", temperature: float = 0.3, retries: int = 3) -> str:
    """Call the configured model with retry + backoff. Returns plain text."""
    last_err = None
    for attempt in range(retries):
        try:
            return _PROVIDERS[PROVIDER](prompt, system, temperature)
        except Exception as e:  # rate limit, network, etc.
            last_err = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"LLM call failed after {retries} attempts: {last_err}")


def call_llm_json(prompt: str, system: str = "", temperature: float = 0.2):
    """Ask for JSON and parse it robustly (strips ```json fences, finds first {...} or [...])."""
    system = (system + "\nReturn ONLY valid JSON. No markdown, no commentary.").strip()
    for _ in range(2):
        raw = call_llm(prompt, system, temperature)
        cleaned = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"(\{.*\}|\[.*\])", cleaned, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass
        prompt += "\n\nYour previous reply was not valid JSON. Reply with valid JSON only."
    raise ValueError("Model did not return valid JSON")


def model_label() -> str:
    """Use this string when the submission form asks which model you used."""
    return f"{MODEL} ({PROVIDER})"
