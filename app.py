from flask import Flask, request, render_template, Response
import os
from atbash import atbash  

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if not file:
        return "No file uploaded"

    original = file.read().decode("utf-8")
    encrypted = atbash(original)

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(save_path, "w") as f:
        f.write(encrypted)

    return "File uploaded & encrypted successfully! <br><a href='/'>Back</a>"


@app.route("/view/<filename>")
def view_encrypted(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "r") as f:
        encrypted = f.read()

    return Response(encrypted, mimetype="text/plain")


@app.route("/download/<filename>")
def download(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "r") as f:
        encrypted = f.read()

    decrypted = atbash(encrypted)

    return Response(
        decrypted,
        mimetype="text/plain",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
