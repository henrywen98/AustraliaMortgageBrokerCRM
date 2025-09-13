import { useState } from 'react'
import api from '../api/client'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [msg, setMsg] = useState('')

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const { data } = await api.post('/auth/login', { email, password })
      localStorage.setItem('access_token', data.access_token)
      setMsg('Logged in')
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || 'Login failed')
    }
  }
  return (
    <form onSubmit={submit} style={{ padding: 16 }}>
      <h2>Login</h2>
      <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
      <button>Login</button>
      <div>{msg}</div>
    </form>
  )
}

