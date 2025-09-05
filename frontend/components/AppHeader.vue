<template>
  <nav class="border-b border-white/10 bg-night/80 backdrop-blur sticky top-0 z-10 text-black">
    <div class="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
      <NuxtLink to="/" class="font-semibold">🍿 PopCornNote</NuxtLink>

      <div class="flex items-center gap-3">
        <!-- Se NON loggato -->
        <template v-if="!isLoggedIn">
          <NuxtLink to="/login" class="text-sm hover:underline">Login</NuxtLink>
          <NuxtLink to="/register" class="text-sm hover:underline">Register</NuxtLink>
        </template>

        <!-- Se loggato -->
        <template v-else>
          <NuxtLink to="/" class="text-black text-sm hover:underline">Dashboard</NuxtLink>
          <NuxtLink to="/news" class="text-black text-sm hover:underline">News</NuxtLink>
          <button class="text-black text-sm px-3 py-1 rounded bg-cinem" @click="onLogout">
            Logout
          </button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
/**
 * Leggiamo direttamente il cookie qui. Questo evita eventuali
 * problemi di idratazione/propagazione dello stato tra composables.
 */
const token = useCookie('token', { sameSite: 'lax', path: '/', watch: true })
const isLoggedIn = computed(() => !!token.value)

const { logout } = useAuth()
function onLogout() {
  if (isLoggedIn.value) logout()
}
</script>
