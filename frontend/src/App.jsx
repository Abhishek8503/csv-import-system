import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import UploadForm from './components/UploadForm'
import JobStatus from './components/JobStatus'

function App() {
  const [count, setCount] = useState(0)
  const [jobId, setJobId] = useState(null);

  return (
    <>
    <div style={{padding: '2rem'}}>
      <h2>CSV Import System</h2>
      <UploadForm onJobCreated={setJobId} />
      <JobStatus jobId={jobId} />
    </div>
      {/* <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p> */}
    </>
  )
}

export default App
