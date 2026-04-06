#!/usr/bin/env bash
set -euo pipefail

L4L_OCI_ROOT="${L4L_OCI_ROOT:-$HOME/git/l4l-oci}"
L4L_OCI_URL="${L4L_OCI_URL:-http://127.0.0.1:8765/mcp}"
L4L_OCI_DEFAULT_MODEL="${L4L_OCI_DEFAULT_MODEL:-qwen-openrouter}"
L4L_OCI_LOG_FILE="${L4L_OCI_LOG_FILE:-$L4L_OCI_ROOT/logs/l4l-oci-service.log}"
L4L_OCI_PID_FILE="${L4L_OCI_PID_FILE:-$L4L_OCI_ROOT/.l4l-oci/l4l-oci.pid}"

PY="$L4L_OCI_ROOT/.venv/bin/python"
if [ ! -x "$PY" ]; then
  echo "ERROR: Python not found at $PY" >&2
  exit 1
fi

if [ -z "${OPENROUTER_API_KEY:-}" ] && [ -z "${QWEN_API_KEY:-}" ]; then
  echo "ERROR: Neither OPENROUTER_API_KEY nor QWEN_API_KEY is set." >&2
  exit 1
fi

health_ok() {
  "$PY" - <<'PY'
import asyncio
import os
from fastmcp import Client

url = os.environ["L4L_OCI_URL"]

async def main() -> int:
    try:
        async with Client(url) as client:
            res = await client.call_tool("health", {})
        status = (res.data or {}).get("status")
        return 0 if status == "ok" else 1
    except Exception:
        return 1

raise SystemExit(asyncio.run(main()))
PY
}

export L4L_OCI_URL

if health_ok; then
  echo "l4l-oci already reachable at $L4L_OCI_URL"
  exit 0
fi

if [ -f "$L4L_OCI_PID_FILE" ]; then
  OLD_PID="$(cat "$L4L_OCI_PID_FILE" 2>/dev/null || true)"
  if [ -n "$OLD_PID" ] && ! kill -0 "$OLD_PID" 2>/dev/null; then
    rm -f "$L4L_OCI_PID_FILE"
  fi
fi

mkdir -p "$(dirname "$L4L_OCI_LOG_FILE")" "$(dirname "$L4L_OCI_PID_FILE")"

(
  cd "$L4L_OCI_ROOT"
  export L4L_OCI_DEFAULT_MODEL
  nohup "$PY" -m l4l_oci >>"$L4L_OCI_LOG_FILE" 2>&1 &
  echo "$!" >"$L4L_OCI_PID_FILE"
)

for _ in $(seq 1 30); do
  if health_ok; then
    echo "l4l-oci started at $L4L_OCI_URL"
    exit 0
  fi
  sleep 0.5
done

echo "ERROR: l4l-oci did not become healthy. Last log lines:" >&2
tail -n 40 "$L4L_OCI_LOG_FILE" >&2 || true
exit 1
