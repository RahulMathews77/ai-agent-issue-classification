from tools import retrieve_tool, classify_tool, tag_tool, confidence_tool
from llm import generate_reasoning  # NEW

def get_root_cause_and_action(category):
    mapping = {
        "Assembly / Joint Integrity Error": (
            "Likely caused by improper fastening, torque issues, or installation error",
            "Inspect joint integrity, verify torque standards, and retrain technicians if needed"
        ),
        "Equipment / Tool Failure": (
            "Likely caused by tool wear, poor maintenance, or incorrect tool usage",
            "Inspect the equipment, verify maintenance history, and replace or recalibrate if required"
        ),
        "Design / Engineering Issue": (
            "Likely caused by design mismatch, drawing error, or specification gap",
            "Review engineering documents, validate specifications, and update process instructions"
        ),
        "Inspection Gap": (
            "Likely caused by missed verification steps or incomplete inspection coverage",
            "Strengthen inspection checkpoints and ensure checklist compliance"
        ),
        "Logistics Damage": (
            "Likely caused by mishandling during transport or inadequate packaging protection",
            "Inspect shipment handling process and strengthen packaging controls"
        ),
        "Human Factors": (
            "Likely caused by insufficient training, inattention, or execution error",
            "Provide targeted retraining and reinforce task-level quality checks"
        ),
        "Power Control Failure": (
            "Likely caused by unstable supply, loose connections, or control unit malfunction",
            "Inspect electrical connections, verify supply stability, and test the control unit"
        ),
        "Vendor Issue": (
            "Likely caused by incorrect supplied material or nonconforming vendor output",
            "Quarantine affected material and raise a vendor quality review"
        ),
        "Incompletion or Loose End": (
            "Likely caused by incomplete handoff or unfinished task execution",
            "Verify task completion before shift handoff and improve closure checks"
        ),
        "Environmental / Site Condition": (
            "Likely caused by temperature, humidity, or adverse site conditions",
            "Review environmental controls and assess material suitability for site conditions"
        ),
        "Construction Trade Impact": (
            "Likely caused by dependency or coordination issues with parallel teams",
            "Improve cross-team coordination and sequence planning"
        ),
        "Obstructive Installation": (
            "Likely caused by restricted access or workspace obstruction",
            "Resolve access constraints and replan installation sequence"
        ),
        "Maintenance Error": (
            "Likely caused by incomplete or incorrect maintenance execution",
            "Review maintenance checklist adherence and retrain where required"
        ),
        "Management Error": (
            "Likely caused by planning gaps, outdated instructions, or change control issues",
            "Review planning process and update procedures to reflect current requirements"
        ),
        "Poor Workmanship": (
            "Likely caused by inconsistent execution quality or insufficient process adherence",
            "Review workmanship standards and increase quality inspection coverage"
        ),
        "Installation Issue": (
            "Likely caused by incorrect installation sequence or improper fitting method",
            "Validate installation steps and reinforce task-specific guidance"
        )
    }

    return mapping.get(
        category,
        ("Likely due to process gap or execution issue",
         "Recommend inspection and corrective training")
    )


def agent(issue_text):
    similar_cases = retrieve_tool(issue_text)
    confidence = confidence_tool(similar_cases)

    if confidence < 0.20:
        return {
            "input": issue_text,
            "category": "Uncertain",
            "tags": [],
            "root_cause": "Low-confidence match. The input does not strongly align with known issue patterns.",
            "action": "Manual review required",
            "similar_cases": similar_cases,
            "confidence": confidence
        }

    category = classify_tool(similar_cases)
    tags = tag_tool(similar_cases)

    # fallback logic (IMPORTANT)
    fallback_root_cause, fallback_action = get_root_cause_and_action(category)

    try:
        # 🔥 LLM CALL
        root_cause, action = generate_reasoning(
            issue_text=issue_text,
            category=category,
            tags=tags,
            similar_cases=similar_cases
        )
    except Exception:
        # fallback if LLM fails
        root_cause, action = fallback_root_cause, fallback_action

    return {
        "input": issue_text,
        "category": category,
        "tags": tags,
        "root_cause": root_cause,
        "action": action,
        "similar_cases": similar_cases,
        "confidence": confidence
    }