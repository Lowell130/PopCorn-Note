<template>
  <button
    @click="toggleWatchlist"
    :disabled="loading"
    class="inline-flex items-center gap-2 px-4 py-2 font-medium transition-all rounded-lg"
    :class="[
      isInWatchlist
        ? 'bg-red-500/10 text-red-500 border border-red-500/50 hover:bg-red-500/20'
        : 'bg-white/10 text-white border border-white/20 hover:bg-white/20'
    ]"
  >
    <svg
      v-if="loading"
      class="w-5 h-5 animate-spin"
      viewBox="0 0 24 24"
      fill="none"
    >
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
    <svg
      v-else-if="isInWatchlist"
      class="w-5 h-5"
      fill="currentColor"
      viewBox="0 0 24 24"
    >
      <path d="M17 3H7c-1.1 0-2 .9-2 2v16l7-3 7 3V5c0-1.1-.9-2-2-2z"/>
    </svg>
    <svg
      v-else
      class="w-5 h-5"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
    </svg>
    
    <span>{{ isInWatchlist ? 'Rimuovi' : 'Salva' }}</span>
  </button>
</template>

<script setup>
const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  type: {
    type: String, // 'movie' | 'tv'
    required: true
  }
})

const { user, fetchMe } = useAuth()
const { apiFetch } = useApi()
const toast = useToast?.()
const loading = ref(false)

const isInWatchlist = computed(() => {
  if (!user.value?.watchlist) return false
  return user.value.watchlist.some(w => w.id === String(props.item.id))
})

async function toggleWatchlist() {
  if (!user.value) {
    navigateTo('/login')
    return
  }

  loading.value = true
  try {
    if (isInWatchlist.value) {
      // Rimuovi
      await apiFetch(`/watchlist/${props.item.id}`, { method: 'DELETE' })
      if (toast?.show) toast.show('success', 'Rimosso dalla Watchlist')
    } else {
      // Aggiungi
      await apiFetch('/watchlist', {
        method: 'POST',
        body: {
          id: String(props.item.id),
          type: props.type,
          title: props.item.title || props.item.name,
          poster: getPosterPath(props.item),
          release_year: props.item.release_date || props.item.first_air_date
        }
      })
      if (toast?.show) toast.show('success', 'Aggiunto alla Watchlist')
    }
    // Ricarica utente per aggiornare lo stato locale
    await fetchMe()
  } catch (e) {
    console.error(e)
    if (toast?.show) toast.show('error', 'Errore aggiornamento Watchlist')
  } finally {
    loading.value = false
  }
}

function getPosterPath(item) {
  // Se abbiamo il path diretto (es. da TMDB raw)
  if (item.poster_path) return item.poster_path
  
  // Se abbiamo URL completo (es. dal nostro backend /movies/xyz)
  if (item.poster_url) {
    try {
      const url = new URL(item.poster_url)
      // Extract filename from TMDB URL
      // es. https://image.tmdb.org/t/p/original/abc.jpg -> /abc.jpg
      const parts = url.pathname.split('/')
      const filename = parts[parts.length - 1]
      return filename ? `/${filename}` : null
    } catch (e) {
      return null
    }
  }
  return null
}
</script>
