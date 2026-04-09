#!/usr/bin/env python3
"""Web UI controller for voice_changer.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from flask import Flask, redirect, render_template_string, request, url_for

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "web_settings.json"

DEFAULT_SETTINGS: dict[str, Any] = {
    "preset": "male_to_female",
    "semitones": 4.0,
    "highpass_hz": 70.0,
    "blocksize": 512,
    "channels": 1,
    "gain_db": 0.0,
    "input_device": "",
    "output_device": "",
    "no_gate": False,
}

app = Flask(__name__)
VOICE_PROCESS: subprocess.Popen[str] | None = None


def load_settings() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        save_settings(DEFAULT_SETTINGS)
        return dict(DEFAULT_SETTINGS)
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        loaded = json.load(f)
    merged = dict(DEFAULT_SETTINGS)
    merged.update(loaded)
    return merged


def save_settings(settings: dict[str, Any]) -> None:
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def build_command(settings: dict[str, Any]) -> list[str]:
    cmd = [
        sys.executable,
        "voice_changer.py",
        "--preset",
        str(settings["preset"]),
        "--semitones",
        str(settings["semitones"]),
        "--highpass-hz",
        str(settings["highpass_hz"]),
        "--blocksize",
        str(settings["blocksize"]),
        "--channels",
        str(settings["channels"]),
        "--gain-db",
        str(settings["gain_db"]),
    ]
    if settings.get("no_gate"):
        cmd.append("--no-gate")
    if str(settings.get("input_device", "")).strip():
        cmd.extend(["--input-device", str(settings["input_device"]).strip()])
    if str(settings.get("output_device", "")).strip():
        cmd.extend(["--output-device", str(settings["output_device"]).strip()])
    return cmd


def process_status() -> str:
    global VOICE_PROCESS
    if VOICE_PROCESS is None:
        return "stopped"
    if VOICE_PROCESS.poll() is None:
        return "running"
    VOICE_PROCESS = None
    return "stopped"


PAGE = """
<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Voice Changer Web設定</title>
  <style>
    body { font-family: "Segoe UI", sans-serif; max-width: 860px; margin: 2rem auto; padding: 0 1rem; }
    h1 { margin-bottom: .5rem; }
    .card { border: 1px solid #ddd; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; }
    .grid { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: .75rem; }
    label { display: block; font-size: .9rem; margin-bottom: .2rem; }
    input, select { width: 100%; padding: .45rem; border: 1px solid #bbb; border-radius: 8px; }
    .row { display: flex; gap: .5rem; align-items: center; }
    .btn { border: 0; border-radius: 8px; padding: .6rem .9rem; cursor: pointer; }
    .save { background:#0f766e; color:#fff; }
    .start { background:#2563eb; color:#fff; }
    .stop { background:#dc2626; color:#fff; }
    .status-running { color:#166534; font-weight: 600; }
    .status-stopped { color:#991b1b; font-weight: 600; }
    .hint { color:#555; font-size:.9rem; }
  </style>
</head>
<body>
  <h1>Voice Changer Web設定</h1>
  <p class="hint">保存後に「Start」で起動。実行中に設定変更したら Stop → Start してください。</p>
  <div class="card">
    <div>状態:
      {% if status == "running" %}
      <span class="status-running">RUNNING</span>
      {% else %}
      <span class="status-stopped">STOPPED</span>
      {% endif %}
    </div>
  </div>
  <form method="post" action="/save" class="card">
    <div class="grid">
      <div>
        <label>Preset</label>
        <select name="preset">
          {% for p in ["male_to_female", "female_to_male", "custom"] %}
            <option value="{{p}}" {% if settings.preset == p %}selected{% endif %}>{{p}}</option>
          {% endfor %}
        </select>
      </div>
      <div>
        <label>Semitones</label>
        <input name="semitones" type="number" step="0.1" value="{{settings.semitones}}" />
      </div>
      <div>
        <label>Highpass Hz</label>
        <input name="highpass_hz" type="number" step="1" value="{{settings.highpass_hz}}" />
      </div>
      <div>
        <label>Blocksize</label>
        <input name="blocksize" type="number" step="1" value="{{settings.blocksize}}" />
      </div>
      <div>
        <label>Channels</label>
        <input name="channels" type="number" min="1" max="2" value="{{settings.channels}}" />
      </div>
      <div>
        <label>Gain dB</label>
        <input name="gain_db" type="number" step="0.1" value="{{settings.gain_db}}" />
      </div>
      <div>
        <label>Input Device (id/name)</label>
        <input name="input_device" type="text" value="{{settings.input_device}}" />
      </div>
      <div>
        <label>Output Device (id/name)</label>
        <input name="output_device" type="text" value="{{settings.output_device}}" />
      </div>
    </div>
    <div class="row" style="margin-top:.75rem;">
      <input id="no_gate" name="no_gate" type="checkbox" {% if settings.no_gate %}checked{% endif %} />
      <label for="no_gate" style="margin:0;">No Gate</label>
    </div>
    <div class="row" style="margin-top:1rem;">
      <button class="btn save" type="submit">Save Settings</button>
    </div>
  </form>

  <div class="card row">
    <form method="post" action="/start"><button class="btn start" type="submit">Start</button></form>
    <form method="post" action="/stop"><button class="btn stop" type="submit">Stop</button></form>
  </div>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(PAGE, settings=load_settings(), status=process_status())


@app.post("/save")
def save():
    settings = {
        "preset": request.form.get("preset", "custom"),
        "semitones": float(request.form.get("semitones", 0)),
        "highpass_hz": float(request.form.get("highpass_hz", 70)),
        "blocksize": int(request.form.get("blocksize", 512)),
        "channels": int(request.form.get("channels", 1)),
        "gain_db": float(request.form.get("gain_db", 0)),
        "input_device": request.form.get("input_device", "").strip(),
        "output_device": request.form.get("output_device", "").strip(),
        "no_gate": request.form.get("no_gate") == "on",
    }
    save_settings(settings)
    return redirect(url_for("index"))


@app.post("/start")
def start():
    global VOICE_PROCESS
    if VOICE_PROCESS is None or VOICE_PROCESS.poll() is not None:
        settings = load_settings()
        VOICE_PROCESS = subprocess.Popen(build_command(settings), cwd=str(ROOT))
    return redirect(url_for("index"))


@app.post("/stop")
def stop():
    global VOICE_PROCESS
    if VOICE_PROCESS and VOICE_PROCESS.poll() is None:
        VOICE_PROCESS.terminate()
        VOICE_PROCESS.wait(timeout=3)
    VOICE_PROCESS = None
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
