from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io, os

app = Flask(__name__)

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return {"error": "No image"}, 400
    output = remove(Image.open(request.files["image"].stream))
    buf = io.BytesIO()
    output.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
