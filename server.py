from flask import Flask, request, send_file
from rembg import remove, new_session
from PIL import Image
import io, os

app = Flask(__name__)

# isnet-general-use - me i ri dhe me i sakt per krejt
session = new_session("isnet-general-use")

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    file = request.files.get("image_file") or request.files.get("image")
    if not file:
        return {"error": "No image provided"}, 400
    try:
        img = Image.open(file.stream).convert("RGBA")
        output = remove(img, session=session)
        buf = io.BytesIO()
        output.save(buf, format="PNG")
        buf.seek(0)
        return send_file(buf, mimetype="image/png")
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "model": "isnet-general-use"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
