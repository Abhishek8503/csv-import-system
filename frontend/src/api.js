const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function uploadCSV(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${BASE_URL}/upload/`, {
        method: 'POST',
        body: formData,
    });

    if(!response.ok){
        throw new Error("Upload Failed.");
    }
    return response.json();
}

export async function fetchJobStatus(jobId) {
    const response = await fetch(`${BASE_URL}/${jobId}/`);

    if(!response.ok){
        throw new Error("Failed to fetch job status.");
    }
    return response.json();
}

export async function retryJob(jobId) {
    const response = await fetch(`${BASE_URL}/${jobId}/retry/`, {
        method: "POST",
    });

    if(!response.ok) {
        throw new Error("Retry job failed.");
    }
    return response.json();
}

