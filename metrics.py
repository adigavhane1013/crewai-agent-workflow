import os
import json
from datetime import datetime


def calculate_metrics(topic: str, validation_output: str, verdict: str) -> dict:
    """
    Parses validation output and computes structured metrics.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    total_claims = validation_output.count("CLAIM:")
    verified_yes = validation_output.count("VERIFIED: YES")
    verified_no = validation_output.count("VERIFIED: NO")
    cite_present = validation_output.count("CITE_TAG_PRESENT: YES")
    cite_missing = validation_output.count("CITE_TAG_PRESENT: NO")

    if total_claims == 0:
        verification_rate = 0
        citation_coverage = 0
    else:
        verification_rate = (verified_yes / total_claims) * 100
        citation_coverage = (cite_present / total_claims) * 100

    print("\n" + "═" * 50)
    print("📊 FINAL RUN METRICS")
    print("═" * 50)
    print(f"Total Claims:              {total_claims}")
    print(f"Verified Claims:           {verified_yes}")
    print(f"Unsupported Claims:        {verified_no}")
    print(f"Missing Citations:         {cite_missing}")
    print(f"Verification Rate:         {verification_rate:.2f}%")
    print(f"Citation Coverage:         {citation_coverage:.2f}%")
    print("═" * 50)

    return {
        "topic": topic,
        "timestamp": timestamp,
        "total_claims": total_claims,
        "verified_claims": verified_yes,
        "unsupported_claims": verified_no,
        "missing_citations": cite_missing,
        "verification_rate_percent": round(verification_rate, 2),
        "citation_coverage_percent": round(citation_coverage, 2),
        "verdict": verdict,
    }


def save_metrics(metrics_data: dict):
    """
    Saves per-run metrics JSON and appends to historical log.
    """

    os.makedirs("metrics", exist_ok=True)

    safe_topic = "".join(
        c if c.isalnum() or c == "_" else "_"
        for c in metrics_data["topic"].replace(" ", "_")
    )

    metrics_path = f"metrics/{safe_topic}_{metrics_data['timestamp']}.json"

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=4)

    # Historical log
    history_file = "metrics/history_log.json"

    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    history.append(metrics_data)

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)