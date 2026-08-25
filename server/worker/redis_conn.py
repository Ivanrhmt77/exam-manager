import os
from redis import Redis
from rq import Queue

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", "6379"))

redis_conn = Redis(host=redis_host, port=redis_port)
task_queue = Queue("default", connection=redis_conn)
