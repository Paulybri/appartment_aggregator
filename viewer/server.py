"""Serves the project folder and lets the viewer set the HIDDEN and VIEWED columns of output/prospects.csv.

Usage (from the project root):  python3 viewer/server.py   ->  http://localhost:8000/viewer/
"""
import csv
import json
import os
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "output", "prospects.csv")
LOCK = threading.Lock()


# Layout: SCORE,PRICE,LOCATION,POSTED,LISTING LINK,HIDDEN,VIEWED
URL_COL = 4
FLAG_COLS = {"hidden": 5, "viewed": 6}  # endpoint /api/<name> -> column index


def set_flag(url: str, col: int, value: bool) -> bool:
    """Set a true/false column for the row whose LISTING LINK matches url. Returns True if found."""
    with LOCK:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        found = False
        for row in rows:
            if len(row) > URL_COL and row[URL_COL].strip() == url:
                row.extend(["false"] * (len(FLAG_COLS) + URL_COL + 1 - len(row)))  # pad short rows
                row[col] = "true" if value else "false"
                found = True
        if found:
            fd, tmp = tempfile.mkstemp(dir=os.path.dirname(CSV_PATH), suffix=".csv")
            with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(rows)
            os.replace(tmp, CSV_PATH)
        return found


class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        name = self.path.removeprefix("/api/")
        if not self.path.startswith("/api/") or name not in FLAG_COLS:
            self.send_error(404)
            return
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            ok = set_flag(str(body["url"]), FLAG_COLS[name], bool(body[name]))
        except (ValueError, KeyError, TypeError):
            self.send_error(400, f"Expected JSON {{url, {name}}}")
            return
        if not ok:
            self.send_error(404, "Listing not found in prospects.csv")
            return
        self.send_response(204)
        self.end_headers()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    server = ThreadingHTTPServer(("127.0.0.1", port), partial(Handler, directory=ROOT))
    print(f"Serving on http://localhost:{port}/viewer/")
    server.serve_forever()
