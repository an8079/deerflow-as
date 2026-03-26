"""Writer Agent"""
from typing import TypedDict

class WriterState(TypedDict):
    task: str
    context: dict
    results: dict
    errors: list

async def run_writer(state: WriterState) -> WriterState:
    research = state.get("results", {}).get("research", {})
    content = f"# {state['task']}报告\n\n## 研究摘要\n{research.get('findings', [])}\n\n---\n*DeerFlow-X AI团队*"
    return {
        **state,
        "results": {**state.get("results", {}), "content": content, "status": "done"}
    }