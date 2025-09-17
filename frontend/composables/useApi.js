// composables/useApi.js
export const useApi = () => {
  const config = useRuntimeConfig()
  const token = useCookie('token', { sameSite: 'lax' })  // 👈 meglio specificare sameSite
  const router = useRouter()

  const apiFetch = async (path, opts = {}) => {
    // 👇 se non hai il token e stai chiamando /auth/me → evita direttamente
    if (!token.value && path === '/auth/me') {
      return null
    }

    try {
      return await $fetch(path, {
        baseURL: config.public.apiBase,
        headers: {
          ...(opts.headers || {}),
          ...(token.value ? { Authorization: `Bearer ${token.value}` } : {}),
        },
        ...opts,
      })
    } catch (err) {
      // 👇 intercetta 401 solo se NON stai chiamando /auth/me
      if (err?.status === 401 && path !== '/auth/me') {
        token.value = null
        router.push('/login')
      }
      throw err
    }
  }

  return { apiFetch }
}
