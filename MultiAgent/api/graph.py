from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt

from state import BlogState
from agent import get_llm, research_agent, writer_agent, editor_agent

MAX_REVISION = 3


# ==========================================
# NODES
# ==========================================

def researcher_node(state: BlogState):
    """Researcher Agent generates or revises the research outline."""
    llm = get_llm()
    researcher_data = research_agent(
        llm=llm,
        topic=state.topic,
        audience=state.audience,
        raw_context=state.raw_context,
        feedback=state.research_feedback
    )
    state.research = researcher_data
    state.research_feedback = ""
    return state


def human_review_research_node(state: BlogState):
    """Pauses graph and asks the human to approve research outline or provide feedback."""
    decision = interrupt({
        "stage": "researcher_review",
        "research": state.research,
        "instructions": (
            "Reply with 'approve' to continue writing, "
            "or provide specific feedback to revise the research."
        )
    })
    
    if isinstance(decision, dict):
        action = decision.get("action", "approve")
        feedback = decision.get("feedback", "")
    else:
        text = str(decision).strip()
        action = "approve" if text.lower() in ["approve", "approved", "ok", "yes", "process", ""] else "revise"
        feedback = "" if action == "approve" else text

    state.research_feedback = feedback
    return state


def writer_node(state: BlogState):
    """Writer Agent generates or revises the draft."""
    llm = get_llm()
    draft_data = writer_agent(
        llm=llm,
        topic=state.topic,
        audience=state.audience,
        research=state.research,
        feedback=state.draft_feedback
    )
    state.draft = draft_data
    state.draft_feedback = ""
    return state


def human_review_draft_node(state: BlogState):
    """Pauses graph and asks the human to approve draft or send feedback to editor/writer."""
    decision = interrupt({
        "stage": "draft_review",
        "draft": state.draft,
        "instructions": (
            "Reply with 'approve' to finalize and edit, "
            "or provide specific feedback to revise the draft."
        )
    })
    
    if isinstance(decision, dict):
        action = decision.get("action", "approve")
        feedback = decision.get("feedback", "")
    else:
        text = str(decision).strip()
        action = "approve" if text.lower() in ["approve", "approved", "ok", "yes", "process", ""] else "revise"
        feedback = "" if action == "approve" else text

    state.draft_feedback = feedback
    return state


def editor_node(state: BlogState):
    """Editor Agent polishes the final draft."""
    llm = get_llm()
    result = editor_agent(state=state, llm=llm)
    state.final_blog = result["final_blog"]
    return state


# ==========================================
# CONDITIONAL ROUTING EDGES
# ========================================== 

def route_research_review(state: BlogState) -> str:
    """If feedback exists, route back to researcher_node; otherwise move to writer_node."""
    if state.research_feedback:
        return "researcher"
    return "writer"


def route_draft_review(state: BlogState) -> str:
    """If feedback exists, route back to writer_node; otherwise move to editor_node."""
    if state.draft_feedback:
        return "writer"
    return "editor"


# ==========================================
# GRAPH ASSEMBLY
# ==========================================

workflow = StateGraph(BlogState)

# 1. Add Nodes
workflow.add_node("researcher", researcher_node)
workflow.add_node("human_review_research", human_review_research_node)
workflow.add_node("writer", writer_node)
workflow.add_node("human_review_draft", human_review_draft_node)
workflow.add_node("editor", editor_node)

# 2. Add Edges & Conditional Connections
workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "human_review_research")

workflow.add_conditional_edges(
    "human_review_research",
    route_research_review,
    {
        "researcher": "researcher",
        "writer": "writer"
    }
)

workflow.add_edge("writer", "human_review_draft")

workflow.add_conditional_edges(
    "human_review_draft",
    route_draft_review,
    {
        "writer": "writer",
        "editor": "editor"
    }
)

workflow.add_edge("editor", END)


checkpointer = InMemorySaver()
app = workflow.compile(checkpointer=checkpointer)