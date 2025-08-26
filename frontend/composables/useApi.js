// composables/useApi.js
export const useApi = () => {
    const config = useRuntimeConfig()
    const token = useCookie('token') // JWT salvato da useAuth


    const apiFetch = (path, opts = {}) => {
        return $fetch(path, {
            baseURL: config.public.apiBase,
            headers: {
                ...(opts.headers || {}),
                ...(token.value ? { Authorization: `Bearer ${token.value}` } : {})
            },
            ...opts
        })
    }


    return { apiFetch }
}