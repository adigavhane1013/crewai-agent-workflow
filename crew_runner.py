from crewai import Crew
from agents import build_agents
from tasks import create_tasks
from search import search_web


def build_crew(topic: str):
    # --------------------------------------------
    # 1. Build Agents
    # --------------------------------------------
    research_agent, writer_agent, validator_agent = build_agents()

    # --------------------------------------------
    # 2. Fetch Search Context
    # --------------------------------------------
    search_context = search_web(topic)

    # --------------------------------------------
    # 3. Build Tasks (Inject Search Context)
    # --------------------------------------------
    research_task, writer_task, validator_task = create_tasks(
        research_agent,
        writer_agent,
        validator_agent,
        topic,
        search_context
    )

    # --------------------------------------------
    # 4. Create Crew
    # --------------------------------------------
    crew = Crew(
        agents=[research_agent, writer_agent, validator_agent],
        tasks=[research_task, writer_task, validator_task],
        verbose=True
    )

    return crew