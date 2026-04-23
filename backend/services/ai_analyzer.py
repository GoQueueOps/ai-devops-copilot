import os
import json
from openai import OpenAI
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

def load_system_context() -> str:
    context_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "data", "system_context.txt"
    )
    try:
        with open(os.path.normpath(context_path), "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

SYSTEM_CONTEXT = load_system_context()

def analyze_log(log_text: str) -> dict:
    if MOCK_MODE:
        return {
            "cause": "MOCK: Memory limit exceeded due to traffic spike",
            "fix": "MOCK: Increase memory limit or add horizontal pod autoscaling",
            "severity": "high"
        }

    # Search vector DB for relevant documentation
    try:
        from services.vector_search import search_relevant_docs
        relevant_docs = search_relevant_docs(log_text)
    except Exception as e:
        print(f"Vector search skipped: {e}")
        relevant_docs = ""

    # Build enriched prompt
    system_prompt = f"""You are a senior DevOps incident analyst for a Pharma enterprise platform.

=== SYSTEM CONTEXT ===
{SYSTEM_CONTEXT}"""

    if relevant_docs:
        system_prompt += f"""

=== RELEVANT DOCUMENTATION ===
{relevant_docs}

Use the documentation above to give specific fix steps where available."""

    system_prompt += """

Given the log entry, respond ONLY with a JSON object — no explanation, no markdown, no backticks.
Format:
{
  "cause": "specific root cause referencing actual services or documentation",
  "fix": "specific fix referencing runbook steps if available",
  "severity": "low | medium | high | critical"
}

If the log involves payment-service, always set severity to critical."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=300,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this log:\n{log_text}"}
        ]
    )

    raw = response.choices[0].message.content.strip()
    return json.loads(raw)