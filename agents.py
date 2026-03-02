from crewai import Agent
from llms import get_gemini_llm, get_validator_llm


def build_agents():

    # =========================
    # Initialize LLMs ONCE
    # =========================

    research_llm = get_gemini_llm()
    writer_llm = get_gemini_llm()
    validator_llm = get_validator_llm()

    # =========================
    # Research Agent
    # =========================

    research_agent = Agent(
        role="Grounded Research Analyst",
        goal="Extract only facts directly from provided search results.",
        backstory="You never use prior knowledge. Only provided data.",
        verbose=True,
        llm=research_llm,
    )

    # =========================
    # Writer Agent
    # =========================

    writer_agent = Agent(
        role="Citation-Grounded Technical Writer",
        goal="Write documentation where every sentence is traceable to source data.",
        backstory="Unsourced claims are defects.",
        verbose=True,
        llm=writer_llm,
    )

    # =========================
    # Validator Agent
    # =========================

    validator_agent = Agent(
        role="Fact-Check Auditor",
        goal="Audit documentation strictly against ground truth search results.",
        backstory="You verify every claim. No assumptions.",
        verbose=True,
        llm=validator_llm,
    )

    return research_agent, writer_agent, validator_agent