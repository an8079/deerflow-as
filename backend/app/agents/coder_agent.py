"""Coder Agent"""
from typing import TypedDict

class CoderState(TypedDict):
    task: str
    context: dict
    results: dict
    errors: list

async def run_coder(state: CoderState) -> CoderState:
    return {
        **state,
        "results": {
            **state.get("results", {}),
            "code": {
                "files": [{"path": "solution.py", "content": "# AI-generated"}],
                "status": "done"
            }
        }
    }