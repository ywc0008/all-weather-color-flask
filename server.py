from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os
import sys
import subprocess
from src.personal_color_analysis import personal_color


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


def main():
    imgpath = "/upload/5.jpg"
    analysis(imgpath)


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

            if not os.path.exists(app.config["UPLOAD_FOLDER"]):
                os.makedirs(app.config["UPLOAD_FOLDER"])

            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            result = personal_color(file_path)
            print(result)
            return jsonify(
                {
                    "message": "File uploaded and processed successfully",
                    "filename": filename,
                    "result": result,
                }
            )
    return jsonify({"message": "Failed to upload file"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
