"""Beacon Guard -- Live Monitor Dashboard.

Shows a real-time split-screen view for the hackathon demo:
- Left: What the user sees (their screen)
- Right: What Beacon Guard sees (the AI's analysis log)

Also shows live metrics: latency (ms), CPU usage, threat count.

Usage:
    python -m guard.monitor
    # Opens a browser dashboard at http://localhost:8001
"""

import asyncio
import base64
import io
import json
import os
import time
from datetime import datetime
from pathlib import Path

import httpx
import psutil
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.responses import StreamingResponse

try:
    from PIL import ImageGrab, Image
except ImportError:
    print("Install Pillow: pip install Pillow")

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
GEMMA_MODEL = os.getenv("GEMMA_MODEL", "gemma4:e4b")

app = FastAPI(title="Beacon Guard Monitor")

# Shared state
guard_state = {
    "running": False,
    "checks": 0,
    "alerts": 0,
    "last_check_ms": 0,
    "cpu_percent": 0.0,
    "last_result": None,
    "last_screenshot_b64": "",
    "events": [],
}

GUARD_PROMPT = """You are Beacon Guard analyzing a screenshot for security threats.
Look for: phishing URLs, fake login pages, scam pop-ups, dark patterns, social engineering.
Respond in JSON: {"threat_detected": true/false, "confidence": 0-100, "threat_type": "string", "severity": "critical|high|medium|low|none", "description": "string", "details": "string", "recommendation": "string"}
Be conservative. Only flag REAL threats. Normal apps and websites are safe."""


def capture_and_encode(max_size=960):
    """Capture screen and return base64."""
    img = ImageGrab.grab()
    ratio = min(max_size / img.width, max_size / img.height, 1.0)
    if ratio < 1.0:
        img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=70)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


async def analyze(img_b64: str) -> dict:
    """Analyze screenshot with Gemma 4."""
    async with httpx.AsyncClient(timeout=120.0) as client:
        start = time.perf_counter()
        resp = await client.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": GEMMA_MODEL,
                "messages": [
                    {"role": "system", "content": GUARD_PROMPT},
                    {"role": "user", "content": "Analyze this screenshot.", "images": [img_b64]},
                ],
                "stream": False,
                "options": {"num_predict": 512, "temperature": 0.2},
            },
        )
        elapsed_ms = (time.perf_counter() - start) * 1000
        content = resp.json().get("message", {}).get("content", "")

        # Parse JSON
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            brace_start = content.find("{")
            brace_end = content.rfind("}")
            if brace_start != -1 and brace_end != -1:
                try:
                    result = json.loads(content[brace_start:brace_end + 1])
                except json.JSONDecodeError:
                    result = {"threat_detected": False, "confidence": 0, "raw": content}
            else:
                result = {"threat_detected": False, "confidence": 0, "raw": content}

        result["latency_ms"] = round(elapsed_ms)
        return result


async def guard_loop():
    """Background guard loop that updates shared state."""
    guard_state["running"] = True
    last_b64 = ""

    while guard_state["running"]:
        try:
            guard_state["cpu_percent"] = psutil.cpu_percent(interval=0.1)

            img_b64 = capture_and_encode()
            guard_state["last_screenshot_b64"] = img_b64

            # Simple change detection via hash comparison
            if img_b64[:200] == last_b64[:200]:
                await asyncio.sleep(3)
                continue
            last_b64 = img_b64

            guard_state["checks"] += 1
            result = await analyze(img_b64)
            guard_state["last_check_ms"] = result.get("latency_ms", 0)
            guard_state["last_result"] = result

            event = {
                "time": datetime.now().strftime("%H:%M:%S"),
                "check": guard_state["checks"],
                "latency_ms": result.get("latency_ms", 0),
                "cpu": guard_state["cpu_percent"],
                "threat": result.get("threat_detected", False),
                "confidence": result.get("confidence", 0),
                "type": result.get("threat_type", "none"),
                "description": result.get("description", ""),
            }
            guard_state["events"].append(event)
            guard_state["events"] = guard_state["events"][-50:]

            if result.get("threat_detected") and result.get("confidence", 0) >= 85:
                guard_state["alerts"] += 1

        except Exception as e:
            guard_state["events"].append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "error": str(e),
            })

        await asyncio.sleep(5)


@app.on_event("startup")
async def startup():
    asyncio.create_task(guard_loop())


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Beacon Guard -- Live Monitor</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', sans-serif; background: #0a0a0a; color: #e0e0e0; }
.header { background: #111; padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #222; }
.header h1 { font-size: 1.1rem; color: #3b82f6; }
.header .status { display: flex; gap: 24px; font-size: 0.85rem; }
.metric { text-align: center; }
.metric .value { font-size: 1.4rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.metric .label { font-size: 0.7rem; color: #888; text-transform: uppercase; letter-spacing: 0.05em; }
.metric.alert .value { color: #ef4444; }
.metric.latency .value { color: #f59e0b; }
.metric.cpu .value { color: #10b981; }
.metric.checks .value { color: #3b82f6; }
.split { display: grid; grid-template-columns: 1fr 1fr; height: calc(100vh - 52px); }
.panel { padding: 16px; overflow-y: auto; }
.panel-left { border-right: 1px solid #222; display: flex; align-items: center; justify-content: center; background: #050505; }
.panel-left img { max-width: 100%; max-height: 100%; border-radius: 8px; }
.panel-right { background: #0d0d0d; }
.log-title { font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px; }
.log-entry { padding: 8px 12px; border-radius: 6px; margin-bottom: 6px; font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; border-left: 3px solid #333; background: #111; }
.log-entry.threat { border-color: #ef4444; background: #1a0505; }
.log-entry.safe { border-color: #10b981; background: #051a0d; }
.log-entry .time { color: #555; }
.log-entry .tag { padding: 2px 6px; border-radius: 3px; font-size: 0.7rem; font-weight: 600; }
.tag-safe { background: #052e16; color: #10b981; }
.tag-threat { background: #450a0a; color: #ef4444; }
.tag-latency { color: #f59e0b; }
</style>
</head>
<body>
<div class="header">
    <h1>BEACON GUARD -- Live Monitor</h1>
    <div class="status">
        <div class="metric checks"><div class="value" id="checks">0</div><div class="label">Checks</div></div>
        <div class="metric latency"><div class="value" id="latency">--</div><div class="label">Latency (ms)</div></div>
        <div class="metric cpu"><div class="value" id="cpu">--</div><div class="label">CPU %</div></div>
        <div class="metric alert"><div class="value" id="alerts">0</div><div class="label">Alerts</div></div>
    </div>
</div>
<div class="split">
    <div class="panel panel-left"><img id="screenshot" src="" alt="Screen capture"></div>
    <div class="panel panel-right">
        <div class="log-title">Agent Analysis Log</div>
        <div id="log"></div>
    </div>
</div>
<script>
async function poll() {
    try {
        const res = await fetch('/api/guard/state');
        const data = await res.json();
        document.getElementById('checks').textContent = data.checks;
        document.getElementById('latency').textContent = data.last_check_ms + 'ms';
        document.getElementById('cpu').textContent = data.cpu_percent.toFixed(1) + '%';
        document.getElementById('alerts').textContent = data.alerts;
        if (data.last_screenshot_b64) {
            document.getElementById('screenshot').src = 'data:image/jpeg;base64,' + data.last_screenshot_b64;
        }
        const logEl = document.getElementById('log');
        logEl.innerHTML = data.events.slice().reverse().map(e => {
            if (e.error) return `<div class="log-entry"><span class="time">${e.time}</span> ERROR: ${e.error}</div>`;
            const cls = e.threat ? 'threat' : 'safe';
            const tag = e.threat ? `<span class="tag tag-threat">THREAT ${e.confidence}%</span>` : '<span class="tag tag-safe">SAFE</span>';
            return `<div class="log-entry ${cls}"><span class="time">${e.time}</span> #${e.check} ${tag} <span class="tag-latency">${e.latency_ms}ms</span> ${e.description || ''}</div>`;
        }).join('');
    } catch {}
    setTimeout(poll, 2000);
}
poll();
</script>
</body>
</html>"""


@app.get("/api/guard/state")
async def get_state():
    return {
        "running": guard_state["running"],
        "checks": guard_state["checks"],
        "alerts": guard_state["alerts"],
        "last_check_ms": guard_state["last_check_ms"],
        "cpu_percent": guard_state["cpu_percent"],
        "last_result": guard_state["last_result"],
        "last_screenshot_b64": guard_state["last_screenshot_b64"],
        "events": guard_state["events"],
    }


if __name__ == "__main__":
    import uvicorn
    print("Beacon Guard Monitor -- http://localhost:8001")
    print("Split-screen: Left = Your screen, Right = Agent's analysis log")
    print("Metrics: Latency (ms), CPU %, Threat count")
    print()
    uvicorn.run(app, host="0.0.0.0", port=8001)
