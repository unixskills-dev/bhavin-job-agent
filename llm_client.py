import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def call_llm(prompt: str, model: str = "gpt-4.1-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    content = response.choices[0].message.content.strip()
    return content

def call_llm_json(prompt: str, model: str = "gpt-4.1-mini"):
    content = call_llm(prompt, model=model)
    # best effort parse
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # try to extract JSON if there's extra text
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1:
            return json.loads(content[start:end+1])
        raise
