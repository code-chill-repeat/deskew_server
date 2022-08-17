import time
import requests
# import ocrmypdf
import subprocess
from datetime import datetime


# deskew logic and send the status to the backend api server
def deskew_service(file_path: str):
    try:
        print("starting deskew service")
        #time.sleep(10)
        # print(10/0)
        # start the deskew service
        start = time.time()
        print(datetime.now())
        subprocess.run(["ocrmypdf", "--tesseract-timeout", "300", "1.pdf", "op.pdf", "--deskew"], shell=True, check=True)
        # ocrmypdf.ocr("1.pdf", "op.pdf", deskew=True, progress_bar=True)
        end = time.time()
        print(datetime.now())
        print(f"time taken: ", end - start)
        print("deskew completed successfully")
        requests.post("http://localhost:8000/api/deskew_response/",data = {"success":f"Deskewed file: {file_path} successfully"})

    except Exception as e: 
        print(e)
        requests.post("http://localhost:8000/api/deskew_response/",data = {"error":e})
