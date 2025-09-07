// composables/useApi.js
export const useApi = () => {
  const config = useRuntimeConfig()
  const token = useCookie('token')
  const router = useRouter()

  const apiFetch = async (path, opts = {}) => {
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
      // Se il token non è valido/scaduto → logout/redirect
      if (err?.status === 401) {
        token.value = null
        router.push('/login')
      }
      throw err
    }
  }

  return { apiFetch }
}
