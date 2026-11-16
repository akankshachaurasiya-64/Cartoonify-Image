"""Flask web app: upload image -> get cartoon version."""
import base64
import os

import cv2
import numpy as np
from flask import Flask, render_template, request

from cartoonify import cartoonify

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB upload limit
ALLOWED = {"png", "jpg", "jpeg", "webp"}


def to_data_uri(img):
    ok, buf = cv2.imencode(".png", img)
    return "data:image/png;base64," + base64.b64encode(buf).decode()


@app.route("/", methods=["GET", "POST"])
def index():
    original = cartoon = error = None
    style = "classic"
    if request.method == "POST":
        file = request.files.get("image")
        style = request.form.get("style", "classic")
        colors = int(request.form.get("colors", 8))
        try:
            if not file or file.filename == "":
                raise ValueError("Pehle image select karo.")
            if file.filename.rsplit(".", 1)[-1].lower() not in ALLOWED:
                raise ValueError("Sirf png, jpg, jpeg, webp allowed hai.")
            data = np.frombuffer(file.read(), np.uint8)
            img = cv2.imdecode(data, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Valid image nahi hai.")
            result = cartoonify(img, style=style, colors=max(2, min(colors, 20)))
            original = to_data_uri(cv2.resize(img, (result.shape[1], result.shape[0])))
            cartoon = to_data_uri(result)
        except Exception as exc:
            error = str(exc)
    return render_template("index.html", original=original, cartoon=cartoon,
                           error=error, style=style)


@app.errorhandler(413)
def too_large(_):
    return render_template("index.html", error="File 5 MB se badi hai.", style="classic"), 413


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
