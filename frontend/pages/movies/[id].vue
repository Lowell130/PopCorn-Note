<template>
  <div>
    <div class="mb-4 flex items-center gap-2 text-sm">
      <NuxtLink to="/" class="text-blue-300 hover:underline">← Torna alla dashboard</NuxtLink>
    </div>

    <div v-if="loading" class="opacity-70">Caricamento…</div>
    <div v-else-if="error" class="text-red-400">Errore: {{ error }}</div>
    <div v-else-if="!movie" class="opacity-70">Film non trovato.</div>

    <div v-else class="bg-white text-black rounded-2xl p-5 shadow space-y-4">
      <h1 class="text-2xl font-semibold break-words">{{ movie.title }}</h1>

      <div class="flex flex-col md:flex-row gap-5">
        <img
          v-if="movie.poster_url"
          :src="movie.poster_url"
          alt=""
          class="w-40 h-60 rounded object-cover border self-start"
        />
        <div class="space-y-2 text-sm">
          <div class="flex flex-wrap gap-2 items-center">
            <StatusBadge :status="movie.status" />
            <span v-if="movie.score" class="px-2 py-1 rounded-full bg-gray-100 text-black">
              Score: <strong>{{ movie.score }}/10</strong>
            </span>
            <span v-if="movie.liked" class="px-2 py-1 rounded-full bg-gray-100 text-black">
              Gradimento: <strong>{{ likedLabel(movie.liked) }}</strong>
            </span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-2 mt-2">
            <div v-if="movie.release_year"><span class="text-gray-500">Anno:</span> <span class="font-medium">{{ movie.release_year }}</span></div>
            <div v-if="movie.release_date"><span class="text-gray-500">Uscita:</span> <span class="font-medium">{{ movie.release_date }}</span></div>
            <div v-if="movie.runtime"><span class="text-gray-500">Durata:</span> <span class="font-medium">{{ movie.runtime }} min</span></div>
            <div v-if="movie.director"><span class="text-gray-500">Regia:</span> <span class="font-medium">{{ movie.director }}</span></div>
            <div v-if="movie.cast?.length" class="sm:col-span-2">
              <span class="text-gray-500">Cast:</span> <span class="font-medium">{{ movie.cast.join(', ') }}</span>
            </div>
     
          </div>

                 <!-- Trama -->
<div v-if="movie.overview" class="text-sm text-gray-800 leading-6">
  <div class="text-gray-500 mb-1">Trama: </div>
  <p class="whitespace-pre-line">{{ movie.overview }}</p>
</div>

          <div v-if="movie.note" class="pt-2">
            <div class="text-gray-500 mb-1">Nota</div>
            <p class="text-gray-800 whitespace-pre-line">{{ movie.note }}</p>
          </div>
        </div>





      </div>

      <!-- Azioni -->
      <!-- <div class="pt-3 border-t mt-2 flex flex-wrap gap-2 justify-center">
        <button @click="completeFromTmdb" class="px-3 py-1.5 text-sm rounded-lg border hover:bg-gray-50" :disabled="loadingAction">
          <span v-if="!loadingAction">Completa con TMDb</span>
          <span v-else class="inline-flex items-center gap-1">
            <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4A4 4 0 008 12H4z"/>
            </svg>
            Carico…
          </span>
        </button>
        <NuxtLink :to="`/`" class="px-3 py-1.5 text-sm rounded-lg border hover:bg-gray-50">Torna</NuxtLink>
      </div> -->
    </div>


<!-- Player VixSRC (mostrato solo se c'è tmdb_id) -->
<ClientOnly>
  <div v-if="playerUrl" class="mt-6">
    <div class="text-sm opacity-70 mb-1">Player</div>
    <div class="rounded-xl overflow-hidden border border-white/10 bg-black/20">
      <iframe
        :src="playerUrl"
        class="w-full"
        style="aspect-ratio: 16 / 9"
        frameborder="0"
        allowfullscreen
        referrerpolicy="no-referrer"
      ></iframe>
    </div>
  </div>
</ClientOnly>

  </div>


  
</template>



<script setup>
import StatusBadge from '@/components/StatusBadge.vue'

const route = useRoute()
const { apiFetch } = useApi()
const toast = useToast()

// helper: ObjectId valido (24 hex)
function isValidObjectId(id) {
  return typeof id === 'string' && /^[a-f0-9]{24}$/i.test(id)
}

// Forza remount della pagina per ogni id (extra safety)
definePageMeta({
  key: r => r.params.id
})

// useAsyncData si occupa di pending/error/data e si aggiorna quando cambia la chiave
const movieId = computed(() => String(route.params.id || ''))

const { data: movie, pending: loading, error } = await useAsyncData(
  // chiave unica per ogni id
  () => `movie:${movieId.value}`,
  // funzione di fetch (validazione ID inclusa)
  async () => {
    const id = movieId.value
    if (!isValidObjectId(id)) {
      // alza errore gestibile da Nuxt, mostra "Errore: ID film non valido."
      throw createError({ statusCode: 400, statusMessage: 'ID film non valido.' })
    }
    return await apiFetch(`/movies/${id}`)
  },
  {
    // rifà il fetch quando cambia l'id
    watch: [movieId],
    // se vuoi evitare SSR per questa pagina, puoi mettere server: false
    // server: false
  }
)

// Etichette liked
const likedOptions = [
  { value: 'loved', label: 'Mi è piaciuto molto' },
  { value: 'liked', label: 'Mi è piaciuto' },
  { value: 'okay', label: 'Carino' },
  { value: 'disliked', label: 'Non mi è piaciuto' },
  { value: 'terrible', label: 'Pessimo' }
]
function likedLabel(val) {
  return likedOptions.find(l => l.value === val)?.label || val
}

// Azione TMDb
const loadingAction = ref(false)
async function completeFromTmdb() {
  if (!movie.value) return
  loadingAction.value = true
  try {
    let tmdbId = movie.value.tmdb_id
    if (!tmdbId) {
      const q = window.prompt('Cerca su TMDb:', movie.value.title || '')
      if (!q || !q.trim()) { loadingAction.value = false; return }
      const results = await apiFetch('/tmdb/search', { query: { q: q.trim() } })
      if (!Array.isArray(results) || results.length === 0) {
        toast.show('error', 'Nessun risultato trovato su TMDb.')
        loadingAction.value = false
        return
      }
      const top = results[0]
      if (!window.confirm(`Usare "${top.title}" (${top.release_date || '—'})?`)) {
        loadingAction.value = false
        return
      }
      tmdbId = top.id
    }

    const details = await apiFetch(`/tmdb/details/${tmdbId}`)
    const payload = {
      tmdb_id: details.tmdb_id ?? tmdbId,
      release_date: details.release_date || undefined,
      release_year: details.release_year ?? undefined,
      poster_url: details.poster_url || undefined,
      director: details.director || undefined,
      cast: Array.isArray(details.cast) ? details.cast : undefined,
      runtime: details.runtime ?? undefined
    }
    const updated = await apiFetch(`/movies/${movieId.value}`, { method: 'PUT', body: payload })
    // aggiorna i dati a schermo senza refetch extra
    movie.value = updated
    toast.show('success', 'Dati completati da TMDb.')
  } catch (e) {
    console.error(e)
    toast.show('error', 'Errore durante il completamento da TMDb.')
  } finally {
    loadingAction.value = false
  }
}

const playerUrl = computed(() => {
  const id = movie.value?.tmdb_id
  return id ? `https://vixsrc.to/movie/${id}?lang=it` : null
})


</script>

