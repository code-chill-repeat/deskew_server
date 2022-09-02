import time
import requests
import subprocess
from datetime import datetime
import boto3
from dotenv import load_dotenv
from botocore.client import Config
import os


load_dotenv()
s3 = boto3.resource('s3', config=Config(signature_version='s3v4'),aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))


def deskew_service(file_path: str, file_name: str, s3_dir_name:str, project_id: int):
    """ 
    file_path: file to download from s3
    file_name: <example>.pdf
    s3_dir_name: path to upload the deskewed file
    """

    try:
        print(os.environ.get('AWS_ACCESS_KEY_ID'))
        print(f"file_path: %s" % file_path)
        print(f"file_name: %s" % file_name)
        print(f"s3_dir_name: %s" % s3_dir_name)
        print("Downloading the file: " + file_name)
        s3.Bucket(os.getenv("AWS_STORAGE_BUCKET_NAME")).download_file(file_path, file_name)
        
        # start the deskew service
        print("starting deskew service")
        start = time.time()
        print(datetime.now())
        file_name = file_name.split('.pdf')[0]
        deskewed_file_name = f"{file_name}_deskewed.pdf"
        subprocess.run(["ocrmypdf", "--clean", "--rotate-pages-threshold", "0.1", "--tesseract-timeout", "300", file_name+".pdf", deskewed_file_name, "--deskew", "--force-ocr"], check=True)
        end = time.time()
        print(datetime.now())
        print(f"time taken: ", end - start)
        print("deskew completed successfully")

        # upload the deskewed file to s3
        s3_file_path = f"{s3_dir_name}/{deskewed_file_name}"
        with open(deskewed_file_name, "rb") as file:
            object = s3.Object('pdf-editor-assets-001', s3_file_path).put(Body=file)
            
        requests.post("https://pdf-backend.de/api/deskew_response/",data = {"description": f"Deskewed file: {file_name} successfully", "project_id": project_id, "file_name": file_name+".pdf"})
        os.remove(file_name+".pdf")
        os.remove(deskewed_file_name)
    except Exception as e: 
        print(e)
        requests.post("https://pdf-backend.de/api/deskew_response/",data = {"description":e, "project_id": project_id})
        os.remove(deskewed_file_name)
