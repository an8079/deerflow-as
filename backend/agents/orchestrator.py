"""LangGraph Orchestrator — 核心调度引擎"""
from typing import TypedDict
from langgraph.graph import StateGraph, END

class WorkflowState(TypedDict):
    task: str
    context: dict
    current_node: str
    results: dict
    errors: list
    iteration: int

def create_workflow_graph():
    graph = StateGraph(WorkflowState)
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("research", research_node)
    graph.add_node("writer", writer_node)
    graph.add_node("coder", coder_node)
    graph.add_node("reviewer", reviewer_node)
    graph.set_entry_point("orchestrator")
    graph.add_edge("orchestrator", "research")
    graph.add_edge("research", "writer")
    graph.add_edge("writer", "coder")
    graph.add_edge("coder", "reviewer")
    graph.add_edge("reviewer", END)
    return graph.compile()

def orchestrator_node(state: WorkflowState):
    return {"current_node": "research", "iteration": state.get("iteration", 0) + 1}

def research_node(state: WorkflowState):
    return {"results": {**state.get("results", {}), "research": "done"}}

def writer_node(state: WorkflowState):
    return {"results": {**state.get("results", {}), "writing": "done"}}

def coder_node(state: WorkflowState):
    return {"results": {**state.get("results", {}), "coding": "done"}}

def reviewer_node(state: WorkflowState):
    return {"results": {**state.get("results", {}), "review": "done"}}

if __name__ == "__main__":
    wf = create_workflow_graph()
    result = wf.invoke({"task": "Create landing page", "context": {}, "results": {}, "errors": [], "iteration": 0})
    print("Workflow result:", result)
