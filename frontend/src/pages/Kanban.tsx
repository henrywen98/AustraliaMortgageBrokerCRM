import { useEffect, useState } from 'react'
import api from '../api/client'

type Deal = {
  id: number
  client_id: number
  lender?: string
  loan_type?: string
  amount?: number
  stage: string
  tags: string[]
}

const STAGES = ["Enquiry","Checklist Sent","Submission","Approval","Settlement"]

export default function Kanban() {
  const [deals, setDeals] = useState<Deal[]>([])
  const [msg, setMsg] = useState('')

  const token = localStorage.getItem('access_token')

  const load = async () => {
    try {
      const { data } = await api.get('/deals', { headers: { Authorization: `Bearer ${token}` } })
      setDeals(data)
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || 'Load failed')
    }
  }
  useEffect(() => { load() }, [])

  const move = async (id: number, to_stage: string) => {
    try {
      await api.post(`/deals/${id}/transition`, { to_stage }, { headers: { Authorization: `Bearer ${token}` } })
      await load()
    } catch (e: any) {
      setMsg('Update failed')
    }
  }

  return (
    <div style={{ display: 'flex', gap: 16, padding: 16 }}>
      {STAGES.map(stage => (
        <div key={stage} style={{ flex: 1 }}>
          <h3>{stage}</h3>
          <div style={{ background: '#f7f7f7', minHeight: 200, padding: 8 }}>
            {deals.filter(d=>d.stage===stage).map(d => (
              <div key={d.id} style={{ background: 'white', marginBottom: 8, padding: 8, border: '1px solid #ddd' }}>
                <div>Deal #{d.id}</div>
                <div>{d.lender} {d.loan_type}</div>
                <div>${d.amount || 0}</div>
                <div style={{ display: 'flex', gap: 4, marginTop: 8 }}>
                  {STAGES.filter(s=>s!==stage).map(s => (
                    <button key={s} onClick={()=>move(d.id, s)}>{s}</button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
      <div>{msg}</div>
    </div>
  )
}

