import requests

def generate_reasoning(issue_text, category, tags, similar_cases):
    context = "\n".join(
        [f"- {case['text']} | category={case['category']}" for case in similar_cases]
    )

    prompt = f"""
You are an industrial quality analysis assistant.

Given the issue description, predicted category, tags, and similar historical cases,
generate:
1. A concise likely root cause
2. A concise recommended corrective action

Rules:
- Keep it practical and specific
- Do not invent unrelated details
- Keep each answer to 1 sentence
- Return only in this format:

Root Cause: <text>
Action: <text>

Issue: {issue_text}
Predicted Category: {category}
Tags: {tags}
Similar Cases:
{context}
""".strip()

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )

    response.raise_for_status()
    text = response.json()["response"].strip()

    root_cause = "Unable to generate root cause"
    action = "Manual review required"

    for line in text.splitlines():
        if line.lower().startswith("root cause:"):
            root_cause = line.split(":", 1)[1].strip()
        elif line.lower().startswith("action:"):
            action = line.split(":", 1)[1].strip()

    return root_cause, action