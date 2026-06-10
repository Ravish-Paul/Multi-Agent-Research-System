from state import ResearchState
from agents.researcher import research_agent
from agents.summarizer import summarize_agent
from agents.writer import writer_agent
from agents.fact_checker import fact_checker_agent
from langgraph.graph import StateGraph, START, END


def research_node(state: ResearchState):
    search_result, research = research_agent(
        state["topic"],
        state["pdf_path"]
    )

    return {
        "search_result": search_result,
        "research": research
    }

def route_query(state):

    topic = state["topic"].lower()

    simple_keywords = [
        "who",
        "what",
        "summarize",
        "explain"
    ]

    for word in simple_keywords:

        if topic.startswith(word):

            return "simple"

    return "research"

def fact_checker_node(state: ResearchState):

    verified_research = fact_checker_agent(
        state["research"]
    )

    return {
        "verified_research": verified_research
    }

def summary_node(state: ResearchState):

    summary = summarize_agent(
        state["verified_research"]
    )

    return {
        "summary": summary
    }

def writer_node(state):

    content = state.get(
        "summary",
        state.get("research", "")
    )

    report = writer_agent(content)

    return {
        "report": report
    }

builder = StateGraph(ResearchState)

builder.add_node("research", research_node)
builder.add_node("fact_checker", fact_checker_node)
builder.add_node("summary", summary_node)
builder.add_node("writer", writer_node)

builder.add_edge(START, "research")
builder.add_conditional_edges(
    "research",
    route_query,
    {
        "simple": "writer",
        "research": "fact_checker"
    }
)
builder.add_edge("fact_checker", "summary")
builder.add_edge("summary", "writer")
builder.add_edge("writer", END)

graph = builder.compile()

