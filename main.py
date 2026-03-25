from agent import agent
import json
from datetime import datetime

def save_feedback(issue, predicted, corrected):
    record = {
        "timestamp": datetime.now().isoformat(),
        "issue": issue,
        "predicted_category": predicted,
        "corrected_category": corrected
    }

    try:
        with open("feedback.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(record)

    with open("feedback.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    query = input("Enter issue: ").strip()

    if not query:
        print("No issue entered. Please provide an issue description.")
        raise SystemExit

    result = agent(query)

    print("\n--- AI Agent Output ---")
    print(f"Category: {result['category']}")
    print(f"Confidence: {result['confidence']:.3f}")
    print(f"Tags: {result['tags']}")
    print(f"Root Cause: {result['root_cause']}")
    print(f"Action: {result['action']}")

    print("\nSimilar Cases Used:")
    for i, case in enumerate(result["similar_cases"], 1):
        print(f"{i}. {case['text']} | {case['category']} | score={case['score']:.3f}")

    approve = input("\nDo you approve this classification? (y/n): ").strip().lower()

    if approve == "n":
        correct = input("Enter correct category: ").strip()
        save_feedback(query, result['category'], correct)
        print("Correction saved to feedback.json")
    else:
        print("Classification approved.")