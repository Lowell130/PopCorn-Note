// composables/useAuth.js
export const useAuth = () => {
    const user = useState('auth_user', () => null)
    const token = useCookie('token', { sameSite: 'lax' })
    const { apiFetch } = useApi()


    const isLoggedIn = computed(() => !!token.value)


    async function register(payload) {
        // { email, username, password }
        return await apiFetch('/auth/register', {
            method: 'POST',
            body: payload
        })
    }


    async function login({ email, password }) {
        const res = await apiFetch('/auth/login', {
            method: 'POST',
            body: { email, password }
        })
        token.value = res.access_token
        // opzionale: recupero film/user subito dopo login
        return res
    }


    function logout() {
        token.value = null
        user.value = null
        return navigateTo('/login')
    }


    // opzionale: ping al backend per validare token, qui non esiste endpoint /me
    async function init() {
        // Se vuoi, qui potresti testare il token con una chiamata protetta.
        // In questa versione ci affidiamo solo alla presenza del token.
        if (!token.value) {
            user.value = null
        }
    }


    return { user, token, isLoggedIn, register, login, logout, init }
}