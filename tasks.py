from crewai import Task
from config import STRICT_VERBATIM_MODE


# ===============================
# STRICT VERBATIM BLOCK
# ===============================

STRICT_MODE_TEXT = """
STRICT VERBATIM MODE ENABLED:

1. You MUST use the exact SOURCE_QUOTE text for every claim.
2. Do NOT shorten the quote.
3. Do NOT remove trailing clauses.
4. Do NOT paraphrase.
5. Do NOT summarize.
6. The documentation sentence must match SOURCE_QUOTE exactly.
7. If exact reuse is not possible, OMIT the claim entirely.
"""


def create_tasks(research_agent, writer_agent, validator_agent, topic, search_context):

    strict_block = STRICT_MODE_TEXT if STRICT_VERBATIM_MODE else ""

    # ===============================
    # RESEARCH TASK
    # ===============================

    research_task = Task(
        description=f"""
You are a Grounded Research Analyst.

You are given the following SEARCH RESULTS:

{search_context}

Collect structured facts about: {topic}

You MUST collect facts across ALL of these categories:
1. General facts (what it is, who made it, when)
2. Key features and capabilities
3. Real-world use cases and applications
4. LIMITATIONS, DRAWBACKS, CRITICISMS, or WEAKNESSES

For the Limitations category specifically:
- Look for phrases like: "limitation", "drawback", "weakness", "problem", "issue",
  "criticism", "disadvantage", "slow", "difficult", "not suitable", "lacks", "poor"
- You MUST extract at least 2-3 limitation facts if they exist in the search results
- If no limitations are found in the results, write exactly: "NO LIMITATIONS FOUND IN SOURCES"

For every fact:
- Provide FACT
- Provide SOURCE_QUOTE (verbatim)
- Provide SOURCE_NUM
- Provide CATEGORY (General / Features / UseCases / Limitations)

Only include facts that have direct textual support.
Do not infer or generalize.
""",
        expected_output="Structured fact list with SOURCE_QUOTE, SOURCE_NUM and CATEGORY including at least 2-3 limitations if present in sources.",
        agent=research_agent,
    )

    # ===============================
    # WRITER TASK (STRICT MODE APPLIED)
    # ===============================

    writer_task = Task(
        description=f"""
You are a Citation-Grounded Technical Writer.

{strict_block}

STRICT RULES:
1. Every sentence MUST be traceable to SOURCE_QUOTE.
2. After EACH sentence add:
   [CITE: "exact SOURCE_QUOTE"]
3. Write ONLY supported facts.
4. If a claim cannot use exact SOURCE_QUOTE, omit it.
5. No inference. No summarization. No expansion.
6. Output pure Markdown.

REQUIRED STRUCTURE:

# {topic.upper()}

## Overview
(2-4 sentences, each ending with [CITE: "..."])

## Key Concepts
- Bullet [CITE: "..."]

## Real-World Use Cases
- Bullet [CITE: "..."]

## Limitations
- Bullet [CITE: "..."]

IMPORTANT FOR LIMITATIONS:
- Use the CATEGORY=Limitations facts from the research output.
- If the researcher found real limitations, you MUST include them here as bullets with citations.
- Only write "Insufficient source data for this section." if the researcher explicitly stated "NO LIMITATIONS FOUND IN SOURCES".
""",
        expected_output="Fully structured Markdown documentation with a populated Limitations section.",
        agent=writer_agent,
    )

    # ===============================
    # VALIDATOR TASK
    # ===============================

    validator_task = Task(
        description="""
You are a Fact-Check Auditor.

STEP 1 — STRUCTURAL CHECK:
Verify presence of:
# Title
## Overview
## Key Concepts
## Real-World Use Cases
## Limitations

STEP 2 — CLAIM AUDIT:
For each claim output EXACTLY in this format:

CLAIM:
CITE_TAG_PRESENT: YES/NO
VERIFIED: YES/NO
EVIDENCE: quote or NOT FOUND
VERDICT: PASS/FAIL

STEP 3 — SCORING:

Structure Score (X/10)
Clarity Score (X/10)
Factual Confidence (X/10)

FAIL if:
- Any VERIFIED = NO
- Missing cite tag
- Missing required section
- Limitations section contains only "Insufficient source data" when sources had limitation data

End EXACTLY with:

Structure Score: X/10
Clarity Score: X/10
Factual Confidence: X/10
Verdict: PASS or FAIL
""",
        expected_output="Full structured validation audit with final verdict.",
        agent=validator_agent,
    )

    return research_task, writer_task, validator_task