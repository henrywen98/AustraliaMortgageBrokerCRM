import { useState } from 'react'
import { deriveKeyFromPassphrase, decryptAesGcm } from '../utils/crypto'

export default function Offline() {
  const [msg, setMsg] = useState('')
  const [rows, setRows] = useState<number | null>(null)

  const onFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    const pass = prompt('Enter passphrase to derive AES-256 key')
    if (!pass) return
    try {
      const buf = await file.arrayBuffer()
      const salt = new TextEncoder().encode('ambrcrm-fixed-demo-salt')
      const key = await deriveKeyFromPassphrase(pass, salt)
      const decrypted = await decryptAesGcm(buf, key)
      // In a full implementation, load decrypted SQLite via sql.js and query read-only views
      setMsg('Decrypted bundle length: ' + decrypted.byteLength)
      setRows(0)
    } catch (e: any) {
      setMsg('Failed to decrypt or parse file')
    }
  }
  return (
    <div style={{ padding: 16 }}>
      <h2>Offline Read-only Mode</h2>
      <input type="file" onChange={onFile} />
      <div>{msg}</div>
      {rows !== null && <div>Rows: {rows}</div>}
    </div>
  )
}

