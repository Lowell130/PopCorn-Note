// middleware/auth.js
export default defineNuxtRouteMiddleware(() => {
const token = useCookie('token')
if (!token.value) return navigateTo('/login')
})