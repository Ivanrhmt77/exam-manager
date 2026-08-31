"use client";

import { useState } from "react";

type JobStatus = {
  job_id: string;
  status: string;
  result?: string;
};

export default function Home() {
  const [job, setJob] = useState<JobStatus | null>(null);
  const [loading, setLoading] = useState(false);

  const handleTestJob = async () => {
    setLoading(true);
    setJob(null);

    const res = await fetch("http://localhost:8000/api/v1/test-job", {
      method: "POST",
    });
    const data: JobStatus = await res.json();
    setJob(data);

    pollJobStatus(data.job_id);
  };

  const pollJobStatus = (jobId: string) => {
    const interval = setInterval(async () => {
      const res = await fetch(`http://localhost:8000/api/v1/test-job/${jobId}`);
      const data: JobStatus = await res.json();
      setJob(data);

      if (data.status === "finished" || data.status === "failed") {
        clearInterval(interval);
        setLoading(false);
      }
    }, 1000);
  };

  return (
    <div className="flex h-screen flex-col items-center justify-center gap-20">
      <h1 className="text-8xl font-bold">Hello World</h1>
      <div className="flex flex-col items-center gap-4">
        <button
          onClick={handleTestJob}
          disabled={loading}
          className="cursor-pointer rounded-xl border-r-4 border-b-4 border-amber-500 bg-white px-4 py-2 font-bold text-black hover:bg-gray-200 active:border-r-2 active:border-b-2 disabled:opacity-50"
        >
          {loading ? "Processing..." : "Test Job"}
        </button>

        {job && (
          <div className="text-center">
            <p>Status: {job.status}</p>
            {job.result && <p>Result: {job.result}</p>}
          </div>
        )}
      </div>
    </div>
  );
}
