#!/usr/bin/env python3
from __future__ import annotations

import io
import posixpath
import urllib.parse
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT_DIR / "skills"
HOST = "127.0.0.1"
PORT = 8787

TARGETS = {
    "project-all": [ROOT_DIR],
    "all": [
        SKILLS_DIR / "START_HERE.md",
        SKILLS_DIR / "skript-code-specialist",
        SKILLS_DIR / "javascript-code-specialist",
        SKILLS_DIR / "code-repair-specialist",
    ],
    "skript-code-specialist": [SKILLS_DIR / "skript-code-specialist"],
    "javascript-code-specialist": [SKILLS_DIR / "javascript-code-specialist"],
    "code-repair-specialist": [SKILLS_DIR / "code-repair-specialist"],
}


def iter_files(path: Path):
    if path.is_file():
        if should_skip(path):
            return
        yield path
        return

    for child in sorted(path.rglob("*")):
        if child.is_file() and not should_skip(child):
            yield child


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return ".git" in parts or "__pycache__" in parts


def build_zip(paths: list[Path]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for base in paths:
            for file_path in iter_files(base):
                arcname = file_path.relative_to(ROOT_DIR).as_posix()
                zf.write(file_path, arcname)
    buffer.seek(0)
    return buffer.read()


HTML = """<!doctype html>
<html lang=\"ja\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Skills Download Web</title>
  <style>
    body { font-family: sans-serif; margin: 0; background: #f7f8fa; color: #1f2937; }
    .wrap { max-width: 880px; margin: 40px auto; background: #fff; border-radius: 16px; padding: 24px; box-shadow: 0 12px 24px rgba(0,0,0,.06); }
    h1 { margin-top: 0; }
    .grid { display: grid; gap: 12px; }
    .card { border: 1px solid #e5e7eb; border-radius: 12px; padding: 14px; display: flex; justify-content: space-between; align-items: center; }
    .btn { background: #2563eb; color: white; text-decoration: none; border-radius: 10px; padding: 8px 14px; font-weight: 600; }
    code { background: #eef2ff; padding: 2px 6px; border-radius: 6px; }
  </style>
</head>
<body>
  <main class=\"wrap\">
    <h1>Skills Download Web</h1>
    <p>別アプリで開くために、必要なスキルを ZIP でダウンロードできます。</p>
    <div class=\"grid\">
      <div class=\"card\"><span>このプロジェクトの全ファイル</span><a class=\"btn\" href=\"/download/project-all.zip\">一気にダウンロード</a></div>
      <div class=\"card\"><span>3スキル一式 + ガイド</span><a class=\"btn\" href=\"/download/all.zip\">ダウンロード</a></div>
      <div class=\"card\"><span>skript-code-specialist</span><a class=\"btn\" href=\"/download/skript-code-specialist.zip\">ダウンロード</a></div>
      <div class=\"card\"><span>javascript-code-specialist</span><a class=\"btn\" href=\"/download/javascript-code-specialist.zip\">ダウンロード</a></div>
      <div class=\"card\"><span>code-repair-specialist</span><a class=\"btn\" href=\"/download/code-repair-specialist.zip\">ダウンロード</a></div>
    </div>
    <h2>起動方法</h2>
    <p>ターミナルで次を実行して Web を起動します。</p>
    <p><code>python3 skills/download-web/app.py</code></p>
    <p>その後 <code>http://127.0.0.1:8787</code> をブラウザで開いてください。</p>
  </main>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = posixpath.normpath(parsed.path)

        if path in {"/", "/index.html"}:
            self.respond_html(HTML)
            return

        if path.startswith("/download/") and path.endswith(".zip"):
            key = path[len("/download/") : -len(".zip")]
            if key not in TARGETS:
                self.send_error(404, "Not Found")
                return

            payload = build_zip(TARGETS[key])
            filename = f"{key}.zip"
            self.send_response(200)
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        self.send_error(404, "Not Found")

    def log_message(self, fmt, *args):
        return

    def respond_html(self, html: str):
        payload = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Skills Download Web running at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
