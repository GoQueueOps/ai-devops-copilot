import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

SYSTEM_PROMPT = """You are a senior DevOps incident analyst.
Given a log entry, respond ONLY with a JSON object — no explanation, no markdown, no backticks.
Format:
{
  "cause": "one sentence root cause",
  "fix": "one sentence recommended fix",
  "severity": "low | medium | high | critical"
}"""

def analyze_log(log_text: str) -> dict:
    if MOCK_MODE:
        return {
            "cause": "MOCK: Memory limit exceeded due to traffic spike",
            "fix": "MOCK: Increase memory limit or add horizontal pod autoscaling",
            "severity": "high"
        }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=200,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Analyze this log:\n{log_text}"}
        ]
    )

    raw = response.choices[0].message.content.strip()
    return json.loads(raw)