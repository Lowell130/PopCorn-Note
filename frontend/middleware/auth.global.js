// middleware/auth.global.js
export default defineNuxtRouteMiddleware((to) => {
  const token = useCookie('token')
  const publicPaths = ['/', '/login', '/register', '/privacy', '/terms', '/news']

  // Se non autenticato e si trova su una pagina privata, reindirizza a /login
  if (!token.value && !publicPaths.includes(to.path)) {
    return navigateTo('/login')
  }
})
