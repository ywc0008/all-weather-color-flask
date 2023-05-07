from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

app.config["UPLOAD_FOLDER"] = "uploads/"
app.config["ALLOWED_EXTENSIONS"] = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file_input"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return jsonify({"message": "업로드 성공", "filename": filename})
    return jsonify({"message": "업로드 실패"})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
