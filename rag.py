from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from data import issues

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [i["text"] for i in issues]

print("Encoding historical issues...")
X = model.encode(texts)
print("Retriever ready.")

def retrieve_similar(query, top_k=2):
    q_vec = model.encode([query])
    sims = cosine_similarity(q_vec, X)[0]
    top_indices = sims.argsort()[-top_k:][::-1]

    results = []
    for i in top_indices:
        results.append({
            "text": issues[i]["text"],
            "category": issues[i]["category"],
            "tags": issues[i]["tags"],
            "score": float(sims[i])
        })

    return results