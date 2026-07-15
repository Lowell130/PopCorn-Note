<template>
  <div class="max-w-7xl mx-auto px-6 py-8">
    <h1 class="text-3xl font-extrabold mb-8 text-white tracking-tight">La mia Watchlist</h1>

    <!-- Guide Banner (Explain Watchlist) -->
    <div class="bg-purple-950/20 border border-purple-500/30 p-6 rounded-2xl flex items-start gap-4 shadow-xl backdrop-blur-md mb-8">
      <div class="p-3 bg-purple-500/10 border border-purple-500/20 rounded-xl text-purple-300 flex-shrink-0 select-none">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
        </svg>
      </div>
      <div class="space-y-1 text-left">
        <h4 class="text-sm font-bold text-white">Cos'è la tua Watchlist?</h4>
        <p class="text-xs text-gray-300 leading-relaxed">
          La Watchlist è la tua lista dei desideri personale. Qui vengono salvati i film e le serie TV che hai intenzione di guardare in futuro. 
          Puoi salvare elementi qui cliccando sul segnalibro di aggiunta in Dashboard o sfogliando i titoli caldi della community nella sezione News. 
          Usa questa sezione come promemoria per pianificare le tue prossime serate cinema!
        </p>
      </div>
    </div>

    <div v-if="loading" class="text-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500 mx-auto"></div>
    </div>

    <div v-else-if="!watchlist || watchlist.length === 0" class="text-center py-20 text-gray-400">
      <svg class="w-16 h-16 mx-auto mb-4 opacity-30 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
      </svg>
      <p class="text-xl font-bold text-white">La tua watchlist è vuota.</p>
      <p class="mt-2 text-sm">Salva film e serie per guardarli più tardi.</p>
      <div class="mt-6">
        <NuxtLink to="/dashboard" class="inline-flex px-6 py-2.5 bg-purple-500/20 border border-purple-500/40 text-purple-300 rounded-full font-semibold hover:bg-purple-500/30 transition hover:scale-105 duration-200">
          Sfoglia catalogo
        </NuxtLink>
      </div>
    </div>

    <div v-else class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6">
      <div
        v-for="item in watchlist"
        :key="item.id"
        class="group relative bg-white/5 border border-white/10 rounded-2xl overflow-hidden shadow-lg transition hover:scale-105 hover:shadow-xl hover:z-10"
      >
        <!-- Poster Link -->
        <NuxtLink :to="item.type === 'movie' ? `/movies/${item.id}` : `/tv/${item.id}`" class="block aspect-[2/3] relative">
          <img
            v-if="item.poster"
            :src="`https://image.tmdb.org/t/p/w500${item.poster}`"
            :alt="item.title"
            class="w-full h-full object-cover transition duration-300 group-hover:opacity-75"
            loading="lazy"
          />
          <div v-else class="w-full h-full bg-white/5 flex items-center justify-center text-gray-500">
            N/A
          </div>
          
          <!-- Overlay on Hover -->
          <div class="absolute inset-x-0 bottom-0 p-4 bg-gradient-to-t from-black/90 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end min-h-[50%]">
             <h3 class="font-bold text-white text-sm line-clamp-2 leading-tight">{{ item.title }}</h3>
             <p class="text-gray-300 text-xs mt-1">{{ item.release_year }} • {{ item.type === 'movie' ? 'Film' : 'Serie TV' }}</p>
          </div>
        </NuxtLink>

        <!-- Remove Button (Top Right) -->
        <button
          @click.prevent="removeItem(item.id)"
          class="absolute top-2 right-2 p-1.5 bg-black/60 hover:bg-red-600 text-white rounded-full backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-all transform hover:scale-110"
          title="Rimuovi dalla Watchlist"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ middleware: 'auth' })

const { user, fetchMe } = useAuth()
const { apiFetch } = useApi()
const toast = useToast?.()

const loading = ref(true)

const watchlist = computed(() => {
    // Ordina per data di aggiunta (più recenti prima)
    if (!user.value?.watchlist) return []
    return [...user.value.watchlist].sort((a, b) => new Date(b.added_at) - new Date(a.added_at))
})

onMounted(async () => {
    // Forza refresh user per essere sicuri di avere la watchlist aggiornata
    if (user.value) {
        await fetchMe()
    }
    loading.value = false
})

async function removeItem(id) {
    if (!confirm('Rimuovere questo elemento dalla watchlist?')) return

    try {
        await apiFetch(`/watchlist/${id}`, { method: 'DELETE' })
        // Aggiorna localmente subito per UI snappy (user.watchlist è reattivo dal composable)
        if (user.value && user.value.watchlist) {
            user.value.watchlist = user.value.watchlist.filter(x => x.id !== id)
        }
        if (toast?.show) toast.show('success', 'Rimosso')
    } catch (e) {
        console.error(e)
        if (toast?.show) toast.show('error', 'Errore durante la rimozione')
        // Fallback refresh se fallisce l'update ottimistico (o per sicurezza)
        await fetchMe()
    }
}
</script>
