import sys
from datetime import datetime

from crew_runner import build_crew
from metrics import calculate_metrics, save_metrics
from utils.file_utils import save_report, save_failed_report


def run():
    # ------------------------------------------------------------------
    # 1. ENVIRONMENT
    # ------------------------------------------------------------------

    topic = input("\nEnter a topic to research: ").strip()
    if not topic:
        sys.exit("Error: Topic cannot be empty.")

    # ------------------------------------------------------------------
    # 2. BUILD CREW
    # ------------------------------------------------------------------
    crew = build_crew(topic)

    print("\n🚀 Starting Crew Execution...\n")
    result = crew.kickoff()

    validation_output = result.tasks_output[2].raw
    verdict = "PASS" if "Verdict: PASS" in validation_output else "FAIL"

    # ------------------------------------------------------------------
    # 3. RETRY LOGIC (Controlled Single Retry)
    # ------------------------------------------------------------------
    if verdict == "FAIL":
        print("\n⚠ Validation failed. Retrying once...\n")

        retry_result = crew.kickoff()
        retry_validation_output = retry_result.tasks_output[2].raw

        if "Verdict: PASS" in retry_validation_output:
            print("✅ Retry succeeded.\n")
            result = retry_result
            validation_output = retry_validation_output
            verdict = "PASS"
        else:
            print("\n❌ Retry also failed. Saving debug report...\n")
            save_failed_report(topic, retry_result)
            sys.exit(1)

    # ------------------------------------------------------------------
    # 4. FINAL METRICS
    # ------------------------------------------------------------------
    metrics_data = calculate_metrics(topic, validation_output, verdict)

    # ------------------------------------------------------------------
    # 5. SAVE OUTPUT
    # ------------------------------------------------------------------
    save_metrics(metrics_data)
    save_report(topic, result)

    print("\n✅ Job complete!\n")


if __name__ == "__main__":
    run()