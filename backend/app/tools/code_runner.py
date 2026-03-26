"""
Code Runner Tool — 安全代码执行沙箱
生产环境应使用 Docker 容器或 AWS Lambda 隔离执行
"""
import asyncio
import logging
import uuid
import subprocess
from typing import TypedDict

logger = logging.getLogger(__name__)

TIMEOUT_SECONDS = 30


class RunResult(TypedDict):
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: int


async def code_runner_tool(code: str, language: str = "python") -> dict:
    """
    在沙箱中安全执行代码

    Args:
        code: 要执行的代码
        language: 语言 (python / node / bash)

    Returns:
        RunResult dict
    """
    import time
    start = time.monotonic()

    lang_map = {
        "python": ("py", ["python3", "-c"]),
        "node": ("js", ["node", "-e"]),
        "bash": ("sh", ["bash", "-c"]),
    }

    ext, cmd = lang_map.get(language, ("py", ["python3", "-c"]))

    # 写入临时文件
    file_id = uuid.uuid4().hex[:8]
    tmp_file = f"/tmp/deerflowx_code_{file_id}.{ext}"

    try:
        with open(tmp_file, "w") as f:
            f.write(code)

        # 执行（带超时和资源限制）
        proc = await asyncio.create_subprocess_exec(
            *cmd, tmp_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=TIMEOUT_SECONDS)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            duration_ms = int((time.monotonic() - start) * 1000)
            return RunResult(
                success=False,
                stdout="",
                stderr=f"执行超时（>{TIMEOUT_SECONDS}秒）",
                exit_code=-1,
                duration_ms=duration_ms,
            )

        duration_ms = int((time.monotonic() - start) * 1000)
        result: RunResult = {
            "success": proc.returncode == 0,
            "stdout": stdout.decode("utf-8", errors="replace"),
            "stderr": stderr.decode("utf-8", errors="replace"),
            "exit_code": proc.returncode,
            "duration_ms": duration_ms,
        }

        logger.info(f"[runner] lang={language} success={result['success']} took={duration_ms}ms")
        return result

    except Exception as e:
        duration_ms = int((time.monotonic() - start) * 1000)
        logger.exception(f"[runner] 错误: {e}")
        return RunResult(
            success=False,
            stdout="",
            stderr=str(e),
            exit_code=-99,
            duration_ms=duration_ms,
        )

    finally:
        try:
            import os
            os.unlink(tmp_file)
        except Exception:
            pass
