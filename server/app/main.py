from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rq.job import Job

from worker.redis_conn import task_queue, redis_conn
from worker.tasks.dummy import ping

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/test-job")
def create_test_job():
    job = task_queue.enqueue(ping)
    return {"job_id": job.id, "status": job.get_status()}


@app.get("/test-job/{job_id}")
def get_test_job_status(job_id: str):
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception:
        raise HTTPException(status_code=404, detail="Job not Found")

    return {"job_id": job.id, "status": job.get_status(), "result": job.result}
