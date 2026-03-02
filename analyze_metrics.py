import json
import os
from pathlib import Path

def analyze_history(history_file: str = "metrics/history_log.json"):
    """
    Reads all run history and computes aggregate metrics for resume use.
    Also reads individual JSON files from metrics/ folder as backup.
    """

    runs = []

    # Load from history log
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            runs = json.load(f)
        print(f"✅ Loaded {len(runs)} runs from history_log.json\n")
    else:
        print("⚠ history_log.json not found. Reading individual metric files...\n")
        metrics_dir = Path("metrics")
        for file in metrics_dir.glob("*.json"):
            if file.name == "history_log.json":
                continue
            with open(file, "r", encoding="utf-8") as f:
                runs.append(json.load(f))
        print(f"✅ Loaded {len(runs)} runs from individual files\n")

    if not runs:
        print("❌ No runs found. Please run the system at least once.")
        return

    # ----------------------------------------------------------------
    # AGGREGATE METRICS
    # ----------------------------------------------------------------
    total_runs = len(runs)
    pass_runs = [r for r in runs if r.get("verdict") == "PASS"]
    fail_runs = [r for r in runs if r.get("verdict") == "FAIL"]

    pass_rate = (len(pass_runs) / total_runs) * 100

    avg_verification_rate = sum(r["verification_rate_percent"] for r in runs) / total_runs
    avg_citation_coverage = sum(r["citation_coverage_percent"] for r in runs) / total_runs

    total_claims_all = sum(r["total_claims"] for r in runs)
    total_verified_all = sum(r["verified_claims"] for r in runs)
    total_unsupported_all = sum(r["unsupported_claims"] for r in runs)
    total_missing_citations = sum(r["missing_citations"] for r in runs)

    best_verification = max(r["verification_rate_percent"] for r in runs)
    best_citation = max(r["citation_coverage_percent"] for r in runs)

    topics_covered = list(set(r["topic"] for r in runs))

    # ----------------------------------------------------------------
    # PRINT REPORT
    # ----------------------------------------------------------------
    print("=" * 55)
    print("📊 MULTI-AGENT SYSTEM — AGGREGATE EVALUATION REPORT")
    print("=" * 55)

    print(f"\n🔢 RUN SUMMARY")
    print(f"  Total Runs Completed:        {total_runs}")
    print(f"  Passed Runs:                 {len(pass_runs)}")
    print(f"  Failed Runs:                 {len(fail_runs)}")
    print(f"  Pass Rate:                   {pass_rate:.1f}%")

    print(f"\n✅ VERIFICATION METRICS (across all runs)")
    print(f"  Total Claims Evaluated:      {total_claims_all}")
    print(f"  Total Verified Claims:       {total_verified_all}")
    print(f"  Total Unsupported Claims:    {total_unsupported_all}")
    print(f"  Avg Verification Rate:       {avg_verification_rate:.2f}%")
    print(f"  Best Verification Rate:      {best_verification:.2f}%")

    print(f"\n📎 CITATION METRICS")
    print(f"  Total Missing Citations:     {total_missing_citations}")
    print(f"  Avg Citation Coverage:       {avg_citation_coverage:.2f}%")
    print(f"  Best Citation Coverage:      {best_citation:.2f}%")

    print(f"\n🌐 TOPICS RESEARCHED")
    for t in topics_covered:
        print(f"  - {t}")

    print(f"\n" + "=" * 55)
    print("📝 RESUME-READY BULLET METRICS")
    print("=" * 55)
    print(f"""
Based on your actual data, here are numbers you can use:

1. 'Achieved {avg_verification_rate:.0f}%+ avg verification rate across {total_runs} research runs'
2. 'Maintained {avg_citation_coverage:.0f}%+ citation coverage across {total_claims_all} total claims evaluated'
3. 'System passed validation in {pass_rate:.0f}% of runs with automated retry logic'
4. 'Evaluated {total_claims_all} factual claims across {len(topics_covered)} research topics'
5. 'Reduced hallucination to {total_unsupported_all} unsupported claims out of {total_claims_all} total'
""")

    # Save report
    report = {
        "total_runs": total_runs,
        "pass_rate_percent": round(pass_rate, 2),
        "avg_verification_rate_percent": round(avg_verification_rate, 2),
        "avg_citation_coverage_percent": round(avg_citation_coverage, 2),
        "best_verification_rate_percent": best_verification,
        "best_citation_coverage_percent": best_citation,
        "total_claims_evaluated": total_claims_all,
        "total_verified_claims": total_verified_all,
        "total_unsupported_claims": total_unsupported_all,
        "topics_covered": topics_covered
    }

    with open("metrics/aggregate_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("💾 Aggregate report saved to metrics/aggregate_report.json")


if __name__ == "__main__":
    analyze_history()