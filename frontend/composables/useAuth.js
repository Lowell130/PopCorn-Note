// composables/useAuth.js
export const useAuth = () => {
  // stato condiviso tra le pagine
  const user  = useState('auth_user', () => null)

  // cookie token (path / così vale per tutto il sito)
  const token = useCookie('token', {
    sameSite: 'lax',
    path: '/',           // <— importante
    // secure: process.client && location.protocol === 'https:' // opzionale in prod
  })

  const { apiFetch } = useApi()

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin    = computed(() => !!user.value?.is_admin)   // <— AGGIUNTO

  async function register(payload) {
    return await apiFetch('/auth/register', { method: 'POST', body: payload })
  }

  async function login({ email, password }) {
    const res = await apiFetch('/auth/login', {
      method: 'POST',
      body: { email, password }
    })
    token.value = res.access_token

    // se il backend restituisce già l’utente
    if (res.user) {
      user.value = res.user
    } else {
      await fetchMe() // prende /auth/me
    }
    return res
  }

  async function fetchMe() {
    if (!token.value) {
      user.value = null
      return null
    }
    try {
      const me = await apiFetch('/auth/me')
      user.value = me
      return me
    } catch (e) {
      // token non valido/expired → reset
      user.value = null
      return null
    }
  }

  // da chiamare in layout/app mounted per ripristinare sessione
  async function init() {
    if (token.value && !user.value) {
      await fetchMe()
    }
  }

  function logout() {
    token.value = null
    user.value = null
    return navigateTo('/login')
  }

  return { user, token, isLoggedIn, isAdmin, register, login, logout, init, fetchMe }
}
