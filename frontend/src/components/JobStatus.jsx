import { useState, useEffect } from "react";
import { fetchJobStatus, retryJob } from "../api";

export default function JobStatus({ jobId, onStatusChange }) {
    const [job, setJob] = useState(null);

    useEffect(() => {
        if (!jobId) {
            setJob(null);
            return;
        }

        let timer;

        const poll = async () => {
            try {
                const data = await fetchJobStatus(jobId);
                onStatusChange(data.status)
                setJob(data);
                
                if (data.status === "PENDING" || data.status === "PROCESSING") {
                    timer = setTimeout(poll, 1000);
                }
            } catch (error) {
                // Silently handle errors during polling
            }
        };
        
        // Start polling immediately
        poll();
        
        return () => {
            if (timer) {
                clearTimeout(timer);
            }
        };
    }, [jobId]);

    useEffect(()=> {
        const handleBeforeUnload = (e)=> {
            if(job && (job.status === "PROCESSING" || job.status === "PENDING")){
                e.preventDefault();
                e.returnValue = "";
            }
        };

        window.addEventListener("beforeunload", handleBeforeUnload);

        return ()=> {
            window.removeEventListener("beforeunload", handleBeforeUnload);
        };
    }, [job]);

    if (!jobId || !job) return null;

    return (
        <>
        <div>
            {job && (
                <>
                <h3>Status: {job.status}</h3>
    
                <progress 
                    value={job.progress_percent} 
                    max="100" 
                    style={{
                        width: '100%',
                        height: '20px',
                        marginBottom: '10px'
                    }}
                />
                <p>{job.progress_percent}%</p>
    
                    {job.status === "COMPLETED" && (
                        <p style={{ color: "green" }}>Import completed successfully</p>
                    )}
    
                {job.status === "FAILED" && (
                    <>
                        <p style={{ color: "red" }}>{job.error_message}</p>
                        <button onClick={() => retryJob(jobId)}>Retry</button>
                    </>
                )}
                </>
            )}
        </div>
        </>
    )
}