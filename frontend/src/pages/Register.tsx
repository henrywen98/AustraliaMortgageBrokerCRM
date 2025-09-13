import { useState } from 'react'
import api from '../api/client'

export default function Register() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('Broker')
  const [msg, setMsg] = useState('')

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const token = localStorage.getItem('access_token')
      const { data } = await api.post('/auth/register', { email, password, role }, { headers: { Authorization: `Bearer ${token}` } })
      setMsg('Registered: ' + data.email)
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || 'Register failed (Admin only)')
    }
  }
  return (
    <form onSubmit={submit} style={{ padding: 16 }}>
      <h2>Register (Admin only)</h2>
      <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
      <select value={role} onChange={e=>setRole(e.target.value)}>
        <option>Broker</option>
        <option>Processor</option>
        <option>Admin</option>
      </select>
      <button>Create</button>
      <div>{msg}</div>
    </form>
  )
}

