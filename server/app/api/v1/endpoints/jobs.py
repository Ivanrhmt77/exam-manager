from fastapi import APIRouter, HTTPException
from rq.job import Job

from worker.redis_conn import task_queue, redis_conn
from worker.tasks.dummy import ping

router = APIRouter(prefix="/test-job", tags=["jobs"])


@router.post("")
def create_test_job():
    job = task_queue.enqueue(ping)
    return {"job_id": job.id, "status": job.get_status()}


@router.get("/{job_id}")
def get_test_job_status(job_id: str):
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception:
        raise HTTPException(status_code=404, detail="Job not Found")

    return {"job_id": job.id, "status": job.get_status(), "result": job.result}
