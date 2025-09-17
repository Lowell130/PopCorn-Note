// middleware/admin-only.js
export default defineNuxtRouteMiddleware((to, from) => {
  const { user, isAdmin } = useAuth()
  if (!user.value) return navigateTo('/login')
  if (!isAdmin.value) return navigateTo('/')
})
