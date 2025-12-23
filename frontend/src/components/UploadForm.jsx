import { useState } from "react";
import { uploadCSV } from "../api";

export default function UploadForm({ onJobCreated, jobStatus }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if(!file) return;

        setLoading(true);
        try {
            const job = await uploadCSV(file);
            onJobCreated(job.id);
        } catch (err) {
            alert(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <>
        <form onSubmit={handleSubmit}>
            <input 
                type="file"
                accept=".csv"
                disabled={loading || jobStatus === "PENDING" || jobStatus === "PROCESSING"}
                onChange={(e) => setFile(e.target.files[0])}
            />
            <button type="submit" disabled={loading || jobStatus === "PROCESSING" || jobStatus === "PENDING"}>
                {loading ? 
                    "Uploading..." : jobStatus === "PENDING" || jobStatus === "PROCESSING" 
                    ? "Processing..." : "Upload CSV"}
            </button>
        </form>
        </>
    )
}