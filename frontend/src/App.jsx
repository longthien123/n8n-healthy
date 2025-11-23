import React, { useEffect, useState } from 'react'
import CancelAppointment from './components/CancelAppointment'

export default function App() {
  const [status, setStatus] = useState('loading')

  useEffect(() => {
    fetch('/api/health/')
      .then(res => res.json())
      .then(data => setStatus(data.status))
      .catch(() => setStatus('error'))
  }, [])

  // GIỮ NGUYÊN: Code cũ của bạn
  return (
    <div style={{fontFamily: 'sans-serif', padding: 20}}>
      <h1>n8n-health frontend</h1>
      <p>Backend status: <strong>{status}</strong></p>
    </div>
  )
}
