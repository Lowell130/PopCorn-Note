// middleware/auth.global.js
export default defineNuxtRouteMiddleware((to) => {
  const token = useCookie('token')
  const publicPaths = ['/login', '/register']

  if (!token.value && !publicPaths.includes(to.path)) {
    return navigateTo('/login')
  }
})
