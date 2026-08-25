from rq import Worker
from worker.redis_conn import redis_conn, task_queue

if __name__ == "__main__":
    worker = Worker([task_queue], connection=redis_conn)
    worker.work()
