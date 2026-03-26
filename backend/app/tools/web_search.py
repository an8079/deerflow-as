"""
Web Search Tool — 模拟网络搜索
生产环境可替换为 Tavily / SerpAPI / DuckDuckGo
"""
import asyncio
import logging
from typing import TypedDict

logger = logging.getLogger(__name__)


class SearchResult(TypedDict):
    title: str
    url: str
    snippet: str
    source: str


async def web_search_tool(query: str, top_k: int = 5) -> dict:
    """
    搜索网络，返回结构化结果

    Args:
        query: 搜索关键词
        top_k: 返回结果数量

    Returns:
        {
            "query": str,
            "results": list[SearchResult],
            "total": int,
            "took_ms": int,
        }
    """
    import time
    start = time.monotonic()

    await asyncio.sleep(0.05)  # 模拟网络延迟

    # 模拟搜索结果
    mock_results = [
        SearchResult(
            title=f"{query} - 官方文档",
            url=f"https://docs.example.com/{query.replace(' ', '-')}",
            snippet=f"关于{query}的详细官方文档，包含完整的API参考和使用示例。",
            source="docs",
        ),
        SearchResult(
            title=f"{query} - 技术博客",
            url=f"https://blog.example.com/{query.replace(' ', '-')}",
            snippet=f"深入解析{query}的实现原理和最佳实践，来自一线工程师的经验总结。",
            source="blog",
        ),
        SearchResult(
            title=f"{query} - GitHub",
            url=f"https://github.com/search?q={query.replace(' ', '+')}",
            snippet=f"GitHub上关于{query}的开源项目和代码示例。",
            source="github",
        ),
    ]

    results = mock_results[:top_k]
    took_ms = int((time.monotonic() - start) * 1000)

    logger.info(f"[search] query='{query}' results={len(results)} took={took_ms}ms")

    return {
        "query": query,
        "results": results,
        "total": len(results),
        "took_ms": took_ms,
    }
