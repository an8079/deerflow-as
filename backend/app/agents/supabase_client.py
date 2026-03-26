"""Supabase Database Client"""
from supabase import create_client, Client
import os

_supabase: Client = None

def get_supabase() -> Client:
    global _supabase
    if _supabase is None:
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_KEY", "")
        if not url or not key:
            print("⚠️  SUPABASE credentials not set — using mock")
            return None
        _supabase = create_client(url, key)
    return _supabase

async def save_task(task_id: str, data: dict):
    sb = get_supabase()
    if sb:
        sb.table("tasks").upsert({"id": task_id, **data})
    print(f"✅ Task {task_id} saved")