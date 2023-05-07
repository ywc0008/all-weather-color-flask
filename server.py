from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os
import sys
import subprocess


# 업로드 이미지 경로 처리 함수
def run_image_processing(image_path):
    script_path = "image_processing.py"
    result = subprocess.run(
        [sys.executable, script_path, image_path], capture_output=True, text=True
    )
    return result.stdout


# 퍼스널컬러 진단 코드 실행 함수
def run_main_py(image_path):
    script_path = "main.py"
    result = subprocess.run(
        [sys.executable, script_path, "--image", image_path],
        capture_output=True,
        text=True,
        cwd="src",  # 작업 디렉토리 설정
    )
    return result.stdout


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

app.config["UPLOAD_FOLDER"] = "uploads"
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

            if not os.path.exists(app.config["UPLOAD_FOLDER"]):
                os.makedirs(app.config["UPLOAD_FOLDER"])

            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            result = run_main_py(file_path)
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
