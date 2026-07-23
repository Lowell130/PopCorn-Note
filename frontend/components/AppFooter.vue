<template>
  <footer class="py-16 bg-slate-950/60 border-t border-white/5 relative z-10 text-gray-400 text-sm">
    <div class="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-12 gap-8 md:gap-12 pb-12">
      <!-- Col 1: Brand & Desc -->
      <div class="md:col-span-5 space-y-4">
        <NuxtLink :to="isLoggedIn ? '/dashboard' : '/'" class="flex items-center gap-3 text-2xl font-bold text-white hover:text-purple-400 transition-colors">
          <span>🍿</span> PopCornNote
        </NuxtLink>
        <p class="text-gray-400 leading-relaxed max-w-sm text-xs sm:text-sm">
          PopCornNote è la tua centrale di controllo per film e serie TV. Cerca con TMDb, organizza la tua libreria per stato, analizza i tuoi gusti e condividi con una community di appassionati.
        </p>
      </div>

      <!-- Col 2: Navigation Links -->
      <div class="md:col-span-3 space-y-4">
        <h4 class="text-xs font-semibold text-white uppercase tracking-wider">Applicativo</h4>
        <ul class="space-y-2">
          <li>
            <NuxtLink to="/dashboard" class="hover:text-purple-400 transition-colors">Dashboard</NuxtLink>
          </li>
          <li>
            <NuxtLink to="/watchlist" class="hover:text-purple-400 transition-colors">Watchlist</NuxtLink>
          </li>
          <li>
            <NuxtLink to="/stats" class="hover:text-purple-400 transition-colors">Statistiche</NuxtLink>
          </li>
        </ul>
      </div>

      <!-- Col 3: Social & Content -->
      <div class="md:col-span-2 space-y-4">
        <h4 class="text-xs font-semibold text-white uppercase tracking-wider">Community</h4>
        <ul class="space-y-2">
          <li>
            <NuxtLink to="/community" class="hover:text-purple-400 transition-colors">Feed Globale</NuxtLink>
          </li>
          <li>
            <NuxtLink to="/news" class="hover:text-purple-400 transition-colors">Ultime News</NuxtLink>
          </li>
        </ul>
      </div>

      <!-- Col 4: Legal & API -->
      <div class="md:col-span-2 space-y-4">
        <h4 class="text-xs font-semibold text-white uppercase tracking-wider">Info</h4>
        <p class="text-[11px] text-gray-500 leading-normal">
          Tutti i dati e le immagini dei film sono forniti da <a href="https://www.themoviedb.org" target="_blank" class="text-sky-400 hover:underline">TMDb</a>.
        </p>
      </div>
    </div>

    <!-- Copyright Divider line -->
    <div class="max-w-7xl mx-auto px-6 pt-6 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-gray-500">
      <span>© {{ new Date().getFullYear() }} PopCornNote. Tutti i diritti riservati.</span>
      <span class="flex gap-4">
        <a href="#" class="hover:text-white transition-colors">Privacy</a>
        <a href="#" class="hover:text-white transition-colors">Termini</a>
      </span>
    </div>

    <!-- Pulsante Torna su (Glassmorphic Scroll to Top) -->
    <transition name="fade">
      <button
        v-if="showScrollTop"
        @click="scrollToTop"
        class="fixed bottom-6 right-6 z-50 p-3 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-300 backdrop-blur-md shadow-lg hover:bg-purple-500/20 hover:scale-105 transition-all outline-none"
        aria-label="Torna su"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7"/>
        </svg>
      </button>
    </transition>
  </footer>
</template>

<script setup>
const token = useCookie('token', { sameSite: 'lax', path: '/', watch: true })
const isLoggedIn = computed(() => !!token.value)

const showScrollTop = ref(false)

function scrollToTop() {
  if (import.meta.client) {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

function handleScroll() {
  showScrollTop.value = window.scrollY > 250
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
