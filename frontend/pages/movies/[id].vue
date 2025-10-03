<!-- pages/movies/[id].vue -->
<template>
  <div class="bg-gray-100">
    <!-- <div class="mb-4 flex items-center gap-2 text-sm">
      <NuxtLink to="/" class="text-blue-300 hover:underline">← Torna alla dashboard</NuxtLink>
    </div> -->

    <div v-if="loading" class="opacity-70">Caricamento…</div>
    <div v-else-if="error" class="text-red-400">Errore: {{ error }}</div>
    <div v-else-if="!movie" class="opacity-70">Film non trovato.</div>

   <!-- <div v-else class="relative rounded-2xl overflow-hidden shadow"> -->
    <div v-else class="relative overflow-hidden shadow">
  <!-- Poster come sfondo -->
  <div
    v-if="movie.poster_url"
    class="absolute inset-0 bg-center bg-cover"
    :style="{ backgroundImage: `url(${movie.poster_url})` }"
  ></div>

  <!-- Overlay scuro -->
  <div class="absolute inset-0 bg-black/80"></div>

  <!-- Contenuti -->
  <div class="relative z-10 my-7 p-5 space-y-4 text-white max-w-7xl mx-auto">
    <h1 class="text-2xl font-semibold break-words">
      {{ movie.title }}
      <span class="bg-blue-100 text-blue-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm">
        MOVIE
      </span>
    </h1>

    <div class="flex flex-col md:flex-row gap-5">
      <!-- Poster piccolo a lato (opzionale) -->
      <img
        v-if="movie.poster_url"
        :src="movie.poster_url"
        alt=""
        class="w-40 h-60 rounded object-cover border self-start"
      />

      <div class="space-y-2 text-sm">
        <div class="flex flex-wrap gap-2 items-center">
          <!-- <StatusBadge :status="movie.status" /> -->
          <span v-if="movie.score" class="px-2 py-1 rounded-full bg-white/15 backdrop-blur text-white">
            Score: <strong>{{ movie.score }}/10</strong>
          </span>
          <span v-if="movie.liked" class="px-2 py-1 rounded-full bg-white/15 backdrop-blur text-white">
            Gradimento: <strong>{{ likedLabel(movie.liked) }}</strong>
          </span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-2 mt-2">
          <div v-if="movie.release_year">
            <span class="text-gray-300">Anno:</span>
            <span class="font-medium">{{ movie.release_year }}</span>
          </div>
          <div v-if="movie.release_date">
            <span class="text-gray-300">Uscita:</span>
            <span class="font-medium">{{ movie.release_date }}</span>
          </div>
          <div v-if="movie.runtime">
            <span class="text-gray-300">Durata:</span>
            <span class="font-medium">{{ movie.runtime }} min</span>
          </div>
          <div v-if="movie.director">
            <span class="text-gray-300">Regia:</span>
            <span class="font-medium">{{ movie.director }}</span>
          </div>
          <div v-if="movie.cast?.length" class="sm:col-span-2">
            <span class="text-gray-300">Cast:</span>
            <span class="font-medium">{{ movie.cast.join(', ') }}</span>
          </div>
        </div>

        <!-- Trama -->
        <div v-if="movie.overview" class="text-sm leading-6">
          <div class="text-gray-300 mb-1">Trama</div>
          <p class="whitespace-pre-line">{{ movie.overview }}</p>
        </div>

        <div v-if="movie.note" class="pt-2">
          <div class="text-gray-300 mb-1">Nota</div>
          <p class="whitespace-pre-line">{{ movie.note }}</p>
        </div>
      </div>
    </div>

    <!-- Azioni (se vuoi riattivarle, mantengono lo stile scuro) -->
    <!--
    <div class="pt-3 border-t border-white/20 mt-2 flex flex-wrap gap-2 justify-center">
      <button @click="completeFromTmdb" class="px-3 py-1.5 text-sm rounded-lg border border-white/30 bg-white/10 hover:bg-white/20" :disabled="loadingAction">
        <span v-if="!loadingAction">Completa con TMDb</span>
        <span v-else class="inline-flex items-center gap-1">
          ...
        </span>
      </button>
      <NuxtLink :to="`/`" class="px-3 py-1.5 text-sm rounded-lg border border-white/30 bg-white/10 hover:bg-white/20">Torna</NuxtLink>
    </div>
    -->
  </div>
</div>


<!-- Player VixSRC (mostrato solo se c'è tmdb_id) -->
   <div class="bg-player">
    <div class="max-w-7xl mx-auto px-4 py-6">
<ClientOnly>
  <div v-if="playerUrl" class="my-6">
     <!-- <h3 class="text-lg font-semibold text-black mb-4">Player</h3> -->
    <div class="overflow-hidden border border-white/10 bg-black/20">
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
</div>

<div class="max-w-7xl mx-auto px-4 py-6">
  <!-- Correlati -->
  <RelatedTmdb
    v-if="tmdbIdNum"
    :kind="'movie'"
    :tmdb-id="tmdbIdNum"
  />

  </div>
</div>

  
</template>

<style scoped>
.bg-player {
	background: linear-gradient(-45deg, #000000, #3a3a3a, #000000, #262626);
	background-size: 400% 400%;
	animation: gradient 15s ease infinite;
	
}

@keyframes gradient {
	0% {
		background-position: 0% 50%;
	}
	50% {
		background-position: 100% 50%;
	}
	100% {
		background-position: 0% 50%;
	}
}

</style>

<script setup>
import StatusBadge from '@/components/StatusBadge.vue'
import RelatedTmdb from '@/components/RelatedTmdb.vue'

const route = useRoute()
const { apiFetch } = useApi()
const toast = useToast()

// helper: ObjectId valido (24 hex)
function isValidObjectId(id) {
  return typeof id === 'string' && /^[a-f0-9]{24}$/i.test(id)
}

// Forza remount della pagina per ogni id (extra safety)
definePageMeta({
  layout: 'movies',
  key: r => r.params.id, // forza remount quando cambia l'id
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

const tmdbIdNum = computed(() => {
  const x = movie.value?.tmdb_id
  return typeof x === 'number' ? x : Number(x || 0)
})
</script>

