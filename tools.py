from typing import Any


from rag import retrieve_similar

def retrieve_tool(issue_text):
    return retrieve_similar(issue_text, top_k=2)

def classify_tool(similar_cases):
    categories = [c["category"] for c in similar_cases]
    return max(set(categories), key=categories.count)

def tag_tool(similar_cases):
    tags = []
    for c in similar_cases:
        tags.extend(c["tags"])
    return list[Any](set[Any](tags))

def confidence_tool(similar_cases):
    if not similar_cases:
        return 0.0
    return max(case["score"] for case in similar_cases)