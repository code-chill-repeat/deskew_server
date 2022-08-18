from flask import Flask, request, Response
import subprocess
# impor t boto3
import asyncio
import time
# import ocrmypdf
from rq_queue import create_queue
from services import deskew_service

app = Flask(__name__)
q = create_queue()

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/deskew", methods=["POST"])
def deskew_api():
    data = request.form
    if "file_path" not in data or "file_name" not in data or "s3_dir_name" not in data:
        return Response(status=400)
    q.enqueue(deskew_service, args=(data["file_path"], data["file_name"], data["s3_dir_name"]), job_timeout=1500)
    return Response(status=200)

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
