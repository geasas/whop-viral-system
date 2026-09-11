"""
_common.py — Shared utilities for the open-source viral clipping stack.

Used by: download_source.py, transcribe.py, auto_edit.py, viral_edit.py,
         publish_tiktok.py, publish_instagram.py, publish_youtube.py,
         submit_whop_bounty.py, analytics_dashboard.py, retention_scorecard.py.

Provides:
  - Logging setup (file + console, UTF-8).
  - State manager (key→value JSON store) — prevents re-publishing, tracks submissions.
  - HTTP session with retry + backoff (requests.Session + urllib3 Retry).
  - run() wrapper around subprocess with live logging.
  - ffprobe helpers (duration, dimensions, codec).
  - path helpers.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPTS_DIR.parent
WORKDIR = PROJECT_ROOT / "_pipeline_workdir"
LOG_DIR = PROJECT_ROOT / "logs"
STATE_FILE = PROJECT_ROOT / "_state.json"
CREDS_DIR = PROJECT_ROOT / "creds"
DATA_DIR = PROJECT_ROOT / "data"

for d in (WORKDIR, LOG_DIR, CREDS_DIR, DATA_DIR):
    d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
_LOGGERS: Dict[str, logging.Logger] = {}


def get_logger(name: str = "pipeline", logfile: Optional[str] = None) -> logging.Logger:
    """Idempotent logger factory. logfile defaults to logs/<name>.log."""
    if name in _LOGGERS:
        return _LOGGERS[name]
    lg = logging.getLogger(name)
    lg.setLevel(logging.INFO)
    lg.propagate = False
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                             datefmt="%Y-%m-%d %H:%M:%S")
    # console
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    lg.addHandler(ch)
    # file
    log_path = LOG_DIR / (logfile or f"{name}.log")
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    lg.addHandler(fh)
    _LOGGERS[name] = lg
    return lg


log = get_logger("pipeline")

# ---------------------------------------------------------------------------
# State manager (key→value)
# ---------------------------------------------------------------------------
def state_load() -> Dict[str, Any]:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            log.warning("state file corrupted — starting fresh")
    return {}


def state_save(d: Dict[str, Any]) -> None:
    tmp = STATE_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(d, indent=2, ensure_ascii=False, default=str),
                   encoding="utf-8")
    tmp.replace(STATE_FILE)


def state_set(key: str, value: Any) -> None:
    s = state_load()
    s[key] = {"value": value, "ts": time.time()}
    state_save(s)


def state_get(key: str) -> Optional[Any]:
    s = state_load()
    v = s.get(key)
    return v["value"] if v else None


def state_has(key: str) -> bool:
    return state_get(key) is not None


# ---------------------------------------------------------------------------
# HTTP session with retry + backoff
# ---------------------------------------------------------------------------
def http_session(token: Optional[str] = None,
                 extra_headers: Optional[Dict[str, str]] = None,
                 total_retries: int = 5,
                 backoff_factor: float = 1.5,
                 status_forcelist: Tuple[int, ...] = (429, 500, 502, 503, 504)) -> requests.Session:
    """Build a requests.Session with sensible retry behaviour."""
    s = requests.Session()
    retry = requests.adapters.Retry(
        total=total_retries,
        connect=total_retries,
        read=total_retries,
        status=total_retries,
        backoff_factor=backoff_factor,
        status_forcelist=list(status_forcelist),
        allowed_methods=frozenset(["GET", "POST", "PUT", "DELETE", "PATCH"]),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    headers = {"User-Agent": "whop-clipping-pipeline/1.0 (+https://whop.com)",
               "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if extra_headers:
        headers.update(extra_headers)
    s.headers.update(headers)
    return s


# ---------------------------------------------------------------------------
# subprocess wrapper
# ---------------------------------------------------------------------------
def run(cmd: List[str], *, check: bool = True, capture: bool = False,
        timeout: Optional[int] = None, env: Optional[Dict[str, str]] = None) -> subprocess.CompletedProcess:
    """Run a subprocess with live logging. Returns CompletedProcess."""
    pretty = " ".join(str(c) for c in cmd)
    log.info(f"$ {pretty}")
    return subprocess.run(
        cmd,
        check=check,
        capture_output=capture,
        text=True,
        timeout=timeout,
        env={**os.environ, **(env or {})},
    )


# ---------------------------------------------------------------------------
# ffprobe helpers
# ---------------------------------------------------------------------------
def probe_duration(path: str | Path) -> float:
    p = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture=True, check=True)
    return float(p.stdout.strip())


def probe_dimensions(path: str | Path) -> Tuple[int, int]:
    p = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height",
             "-of", "csv=p=0", str(path)],
            capture=True, check=True)
    w, h = p.stdout.strip().split(",")
    return int(w), int(h)


def probe_audio(path: str | Path) -> bool:
    p = run(["ffprobe", "-v", "error", "-select_streams", "a",
             "-show_entries", "stream=codec_type",
             "-of", "csv=p=0", str(path)],
            capture=True, check=False)
    return "audio" in (p.stdout or "")


# ---------------------------------------------------------------------------
# Small misc helpers
# ---------------------------------------------------------------------------
def env_required(*names: str) -> Dict[str, str]:
    """Read required env vars; raise if any missing. Returns the dict."""
    out = {}
    missing = []
    for n in names:
        v = os.environ.get(n)
        if not v:
            missing.append(n)
        else:
            out[n] = v
    if missing:
        raise SystemExit(f"Missing env vars: {', '.join(missing)}. "
                         f"Copy scripts/.env.template to .env and fill them in.")
    return out


def env_optional(name: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(name) or default


def fmt_time_srt(t: float) -> str:
    """1:00:00.000 SRT timestamp format."""
    ms = int(round((t - int(t)) * 1000))
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    return f"{h:d}:{m:02d}:{s:02d},{ms:03d}"


def fmt_time_ass(t: float) -> str:
    """0:00:00.00 ASS timestamp format."""
    cs = int(round((t - int(t)) * 100))
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"


def write_json(data: Any, path: str | Path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str),
                 encoding="utf-8")


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))
