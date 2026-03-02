import os
from datetime import datetime


def _safe_topic_name(topic: str) -> str:
    return "".join(
        c if c.isalnum() or c == "_" else "_"
        for c in topic.replace(" ", "_")
    )


def save_report(topic: str, result):
    """
    Saves final successful run output as Markdown report.
    """

    os.makedirs("output", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = _safe_topic_name(topic)

    out_path = f"output/{safe_topic}_{timestamp}.md"

    research_output = result.tasks_output[0].raw
    documentation_output = result.tasks_output[1].raw
    validation_output = result.tasks_output[2].raw

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# Automated Report: {topic}\n\n")
        f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("---\n\n")
        f.write("## 1. Research Summary\n\n")
        f.write(research_output)
        f.write("\n\n---\n\n")
        f.write("## 2. Generated Documentation\n\n")
        f.write(documentation_output)
        f.write("\n\n---\n\n")
        f.write("## 3. Validation Audit\n\n")
        f.write(validation_output)

    print(f"\n📄 Report saved → {out_path}\n")


def save_failed_report(topic: str, result):
    """
    Saves failed run for debugging.
    """

    os.makedirs("output/failed", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = _safe_topic_name(topic)

    fail_path = f"output/failed/{safe_topic}_{timestamp}_FAILED.md"

    research_output = result.tasks_output[0].raw
    documentation_output = result.tasks_output[1].raw
    validation_output = result.tasks_output[2].raw

    with open(fail_path, "w", encoding="utf-8") as f:
        f.write(f"# FAILED RUN — {topic}\n\n")
        f.write(f"*{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("---\n\n")
        f.write("## Research Summary\n\n")
        f.write(research_output)
        f.write("\n\n---\n\n")
        f.write("## Generated Documentation (REJECTED)\n\n")
        f.write(documentation_output)
        f.write("\n\n---\n\n")
        f.write("## Validation Audit\n\n")
        f.write(validation_output)

    print(f"\n🛑 Debug report saved → {fail_path}\n")