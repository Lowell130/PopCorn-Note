// middleware/auth.global.js
export default defineNuxtRouteMiddleware((to) => {
  const token = useCookie('token')
  const publicPaths = ['/', '/login', '/register', '/privacy', '/terms', '/news']

  // Se autenticato e prova a tornare sulla landing, mandalo in dashboard
  if (token.value && to.path === '/') {
    return navigateTo('/dashboard')
  }

  // Se non autenticato, consenti solo pagine pubbliche
  if (!token.value && !publicPaths.includes(to.path)) {
    // consenti anche le pagine nidificate pubbliche se necessario in futuro
    return navigateTo('/login')
  }
})
