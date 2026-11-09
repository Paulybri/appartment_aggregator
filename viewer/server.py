"""Serves the project folder and lets the viewer toggle the HIDDEN column of output/prospects.csv.

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


def set_hidden(url: str, hidden: bool) -> bool:
    """Set the HIDDEN column (5th) for the row whose LISTING LINK matches url. Returns True if found."""
    with LOCK:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        found = False
        for row in rows:
            if len(row) >= 4 and row[3].strip() == url:
                row[4:] = ["true" if hidden else "false"]
                found = True
        if found:
            fd, tmp = tempfile.mkstemp(dir=os.path.dirname(CSV_PATH), suffix=".csv")
            with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(rows)
            os.replace(tmp, CSV_PATH)
        return found


class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/hidden":
            self.send_error(404)
            return
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            ok = set_hidden(str(body["url"]), bool(body["hidden"]))
        except (ValueError, KeyError, TypeError):
            self.send_error(400, "Expected JSON {url, hidden}")
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
