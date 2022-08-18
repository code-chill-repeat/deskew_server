import time
import requests
import subprocess
from datetime import datetime
import boto3


def deskew_service(file_path: str, file_name: str, s3_dir_name:str):
    """ 
    file_path: file to download from s3
    file_name: <example>.pdf
    s3_dir_name: path to upload the deskewed file
    """

    try:
        print("Downloading the file: " + file_name)
        s3 = boto3.client('s3')
        s3.download_file('pdf-editor-assets-001', file_path, file_name)
        
        # start the deskew service
        print("starting deskew service")
        start = time.time()
        print(datetime.now())
        file_name = file_name.split('.pdf')[0]
        deskewed_file_name = f"{file_name}_deskewed.pdf"
        subprocess.run(["ocrmypdf", "--tesseract-timeout", "300", file_name, deskewed_file_name, "--deskew"], check=True)
        end = time.time()
        print(datetime.now())
        print(f"time taken: ", end - start)
        print("deskew completed successfully")

        # upload the deskewed file to s3
        s3_file_path = f"{s3_dir_name}/{deskewed_file_name}"
        object = s3.Object('pdf-editor-assets-001', s3_file_path).put(Body=deskewed_file_name)
            
        requests.post("http://localhost:8000/api/deskew_response/",data = {"success":f"Deskewed file: {file_name} successfully"})

    except Exception as e: 
        print(e)
        requests.post("http://localhost:8000/api/deskew_response/",data = {"error":e})
