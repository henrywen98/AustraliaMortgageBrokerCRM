export async function deriveKeyFromPassphrase(passphrase: string, salt: Uint8Array) {
  const enc = new TextEncoder()
  const keyMaterial = await crypto.subtle.importKey('raw', enc.encode(passphrase), 'PBKDF2', false, ['deriveKey'])
  return crypto.subtle.deriveKey({name: 'PBKDF2', salt, iterations: 100000, hash: 'SHA-256'}, keyMaterial, {name: 'AES-GCM', length: 256}, false, ['decrypt'])
}

export async function decryptAesGcm(noncePlusCiphertext: ArrayBuffer, key: CryptoKey) {
  const nonce = new Uint8Array(noncePlusCiphertext.slice(0, 12))
  const ct = noncePlusCiphertext.slice(12)
  const plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: nonce }, key, ct)
  return plain
}

