<!-- pages/login.vue -->
<template>
  <div class="min-h-[80vh] flex items-center justify-center px-4 relative">
    <!-- Ambient glow behind card -->
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 rounded-full bg-purple-500/5 blur-3xl pointer-events-none"></div>

    <div class="max-w-md w-full bg-slate-950/60 border border-white/10 rounded-3xl p-8 backdrop-blur-md shadow-2xl relative overflow-hidden z-10">
      
      <!-- Header -->
      <div class="text-center mb-8">
        <span class="text-3xl block mb-2 select-none">🍿</span>
        <h1 class="text-2xl font-extrabold text-white tracking-tight">Accedi a PopCornNote</h1>
        <p class="text-xs text-gray-400 mt-1">Bentornato! Inserisci i tuoi dati per accedere.</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="submit" class="space-y-4">
        <div>
          <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Indirizzo Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="nome@esempio.com"
            class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all"
            required
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Password</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all"
            required
          />
        </div>

        <div class="pt-2">
          <button
            :disabled="loading"
            :class="[
              'w-full py-3 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/40 text-purple-300 font-bold rounded-xl text-sm transition-all transform active:scale-98 shadow-lg shadow-purple-500/5',
              loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
            ]"
          >
            <span v-if="loading" class="flex items-center justify-center gap-2">
              <svg class="animate-spin h-4 w-4 text-purple-300" viewBox="0 0 24 24" fill="none">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4A4 4 0 008 12H4z"/>
              </svg>
              Accesso in corso...
            </span>
            <span v-else>Accedi</span>
          </button>
        </div>
      </form>

      <!-- Footer Link -->
      <p class="text-xs text-gray-500 text-center mt-6">
        Non hai ancora un account?
        <NuxtLink to="/register" class="text-purple-400 font-semibold hover:underline">Registrati gratis</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
const email = ref("")
const password = ref("")
const loading = ref(false)
const { login } = useAuth()

async function submit() {
  if (loading.value) return
  loading.value = true
  try {
    await login({ email: email.value, password: password.value })
    navigateTo("/dashboard")
  } catch (e) {
    alert("Login fallito")
    console.error(e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
</style>
