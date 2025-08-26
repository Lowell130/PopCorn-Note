let timer // fuori dalla factory così lo condividi tra istanze

export const useToast = () => {
  const msg = useState('toast_msg', () => null)
  const type = useState('toast_type', () => 'success')

  function show(t = 'success', m = '') {
    // normalizza messaggio
    const text = String(m ?? '').trim()
    if (!text) {
      // se non c'è testo, chiudi il toast e stop
      msg.value = null
      return
    }

    type.value = t
    msg.value = text

    // reset timer precedente
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      msg.value = null
    }, 3000)
  }

  // opzionale: esponi un close manuale
  function close() {
    if (timer) clearTimeout(timer)
    msg.value = null
  }

  return { msg, type, show, close }
}
