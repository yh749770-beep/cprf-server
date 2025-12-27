import os
from flask import Flask, request, send_file, abort, Response
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_TOKEN = os.environ.get("UPLOAD_TOKEN", "")
LATEST_PATH = os.path.join(os.path.dirname(__file__), "latest.png")

@app.get("/latest.png")
def latest_png():
    if not os.path.exists(LATEST_PATH):
        abort(404)
    resp = send_file(LATEST_PATH, mimetype="image/png")
    # avoid browser caching
    resp.headers["Cache-Control"] = "no-store, max-age=0"
    return resp

@app.post("/upload")
def upload():
    auth = request.headers.get("Authorization", "")
    if not UPLOAD_TOKEN or auth != f"Bearer {UPLOAD_TOKEN}":
        abort(401)

    if "file" not in request.files:
        abort(400)

    f = request.files["file"]
    if f.filename == "":
        abort(400)

    # save as latest.png always
    f.save(LATEST_PATH)
    return {"ok": True}
