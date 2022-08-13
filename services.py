import time
import requests


# deskew logic and send the status to the backend api server
def deskew_service(file_path: str):
    try:
        print("starting deskew service")
        time.sleep(10)
        # print(10/0)
        print("deskew completed successfully")
        requests.post("http://localhost:8000/api/deskew_response/",data = {"success":f"Deskewed file: {file_path} successfully"})

    except Exception as e: 
        print(e)
        requests.post("http://localhost:8000/api/deskew_response/",data = {"error":e})
