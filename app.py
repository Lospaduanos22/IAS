from flask import Flask, request, render_template, Response
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Atbash Cipher ---
def atbash(text):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr(base + (25 - (ord(char) - base)))
        else:
            result += char
    return result


# --- Home Page ---
@app.route("/")
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)


# --- Upload (encrypt automatically) ---
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


# --- View encrypted file in browser ---
@app.route("/view/<filename>")
def view_encrypted(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "r") as f:
        encrypted = f.read()

    return Response(encrypted, mimetype="text/plain")


# --- Download decrypted file ---
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


# --- Run server on the network ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
