// composables/useAuth.js
export const useAuth = () => {
  const user = useState('auth_user', () => null)
  const token = useCookie('token', { sameSite: 'lax' })
  const { apiFetch } = useApi()

  const isLoggedIn = computed(() => !!token.value)

  async function register(payload) {
    return await apiFetch('/auth/register', { method: 'POST', body: payload })
  }

  async function login({ email, password }) {
    const res = await apiFetch('/auth/login', {
      method: 'POST',
      body: { email, password }
    })
    token.value = res.access_token
    // prendi user dal login se presente, altrimenti fai /auth/me
    if (res.user) {
      user.value = res.user
    } else {
      await fetchMe()
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
      user.value = null
      return null
    }
  }

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

  return { user, token, isLoggedIn, register, login, logout, init, fetchMe }
}
