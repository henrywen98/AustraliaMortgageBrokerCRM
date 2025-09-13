import { useEffect, useState } from 'react'
import api from '../api/client'

export default function Stats() {
  const [summary, setSummary] = useState<any>({})
  const token = localStorage.getItem('access_token')
  useEffect(() => {
    (async () => {
      const { data } = await api.get('/stats/summary', { headers: { Authorization: `Bearer ${token}` } })
      setSummary(data)
    })()
  }, [])
  return (
    <div style={{ padding: 16 }}>
      <h2>Summary</h2>
      <pre>{JSON.stringify(summary, null, 2)}</pre>
    </div>
  )
}

