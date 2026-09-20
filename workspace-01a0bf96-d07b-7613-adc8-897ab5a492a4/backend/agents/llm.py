"""Minimal Gemini client over REST (no SDK dependency). Returns parsed JSON."""
import json
import re
import requests

BASE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
DEFAULT_MODEL = "gemini-2.5-flash"


class LLMError(Exception):
    pass


def _strip_fences(txt):
    txt = txt.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", txt, re.DOTALL)
    if m:
        txt = m.group(1)
    return txt.strip()


def gemini_generate(prompt, api_key, model=None, system=None, temperature=0.2, timeout=90):
    if not api_key:
        raise LLMError("No API key configured")
    model = model or DEFAULT_MODEL
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temperature, "maxOutputTokens": 8192},
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}
    try:
        r = requests.post(BASE.format(model=model), headers=headers, json=body, timeout=timeout)
    except requests.RequestException as e:
        raise LLMError(f"Network error calling Gemini: {e}")
    if r.status_code != 200:
        raise LLMError(f"Gemini API {r.status_code}: {r.text[:200]}")
    data = r.json()
    try:
        parts = data["candidates"][0]["content"]["parts"]
        return "".join(p.get("text", "") for p in parts)
    except (KeyError, IndexError):
        raise LLMError(f"Unexpected Gemini response: {json.dumps(data)[:300]}")


def gemini_json(prompt, api_key, model=None, system=None, temperature=0.2):
    """Ask Gemini for JSON output and parse it."""
    text = gemini_generate(prompt, api_key, model, system, temperature)
    try:
        return json.loads(_strip_fences(text))
    except json.JSONDecodeError:
        # last-resort: extract first {...} block
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                pass
        raise LLMError("Model did not return valid JSON")
