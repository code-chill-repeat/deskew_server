from redis import Redis
from rq import Queue, get_current_job
import requests

# create a new queue
def create_queue():
    q = Queue(connection=Redis())
    return q