import React, { useEffect, useState } from 'react'

export default function App() {
  const [status, setStatus] = useState('loading')

  useEffect(() => {
    fetch('/api/health/')
      .then(res => res.json())
      .then(data => setStatus(data.status))
      .catch(() => setStatus('error'))
  }, [])

  return (
    <div style={{fontFamily: 'sans-serif', padding: 20}}>
      <h1>n8n-health frontend</h1>
      <p>Backend status: <strong>{status}</strong></p>
    </div>
  )
}
