<template>
  <ClientOnly>
    <div class="bg-white text-black rounded-2xl p-5 shadow space-y-3">
      <h2 class="text-lg font-semibold">Cerca da TMDb (opzionale)</h2>

      <div class="flex gap-2">
        <input
          v-model.trim="q"
          placeholder="Cerca titolo..."
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          @keyup.enter="search"
        />
        <button @click="search" class="focus:outline-none text-white bg-purple-700 hover:bg-purple-800 focus:ring-4 focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-purple-600 dark:hover:bg-purple-700 dark:focus:ring-purple-900">Cerca</button>
      </div>

      <div v-if="!apiKey" class="text-sm text-red-600">
        Imposta l’API key TMDb per usare questa funzione.
      </div>

      <div v-if="loading" class="text-sm opacity-70">Ricerca in corso…</div>
      <div v-if="error" class="text-sm text-red-600">Errore: {{ error }}</div>
      <div v-if="!loading && !error && searched && results.length === 0" class="text-sm opacity-70">
        Nessun risultato.
      </div>

      <!-- Mostra la lista solo se showResults è true -->
      <ul v-if="showResults && results.length" class="divide-y">
        <li v-for="r in results" :key="r.id" class="py-2 flex items-center justify-between">
          <div class="min-w-0">
            <div class="font-medium truncate">{{ r.title }}</div>
            <div class="text-xs opacity-70">{{ r.release_date || '—' }}</div>
          </div>
          <button
            @click="pick(r)"
            class="text-sm px-3 py-1 rounded bg-green-600 text-white disabled:opacity-60"
            :disabled="loadingPickId === r.id"
          >
            <span v-if="loadingPickId !== r.id">Usa dati</span>
            <span v-else class="inline-flex items-center gap-1">
              <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4A4 4 0 008 12H4z"/>
              </svg>
              Prendo…
            </span>
          </button>
        </li>
      </ul>
    </div>
  </ClientOnly>
</template>

<script setup>
const emit = defineEmits(['prefill'])

const q = ref('')
const results = ref([])
const loading = ref(false)
const error = ref('')
const searched = ref(false)

// NUOVO: controlla la visibilità della lista
const showResults = ref(false)
// NUOVO: loading per singolo elemento cliccato
const loadingPickId = ref(null)

const config = useRuntimeConfig()
const apiKey = computed(() => config.public.tmdbApiKey)

async function search () {
  error.value = ''
  searched.value = true
  results.value = []
  showResults.value = false

  if (!apiKey.value) { error.value = 'API key mancante'; return }
  if (!q.value.trim()) { error.value = 'Inserisci un titolo'; return }

  loading.value = true
  try {
    const url = new URL('https://api.themoviedb.org/3/search/movie')
    url.searchParams.set('api_key', apiKey.value)
    url.searchParams.set('query', q.value.trim())
    url.searchParams.set('language', 'it-IT')
    url.searchParams.set('include_adult', 'false')
    url.searchParams.set('page', '1')

    const res = await $fetch(url.toString(), { headers: { accept: 'application/json' } })
    results.value = Array.isArray(res?.results) ? res.results.slice(0, 10) : []
    // mostra la lista solo se ci sono risultati
    showResults.value = results.value.length > 0
  } catch (e) {
    console.error('[TMDb] search error:', e)
    error.value = e?.data?.status_message || e?.message || 'Errore sconosciuto'
  } finally {
    loading.value = false
  }
}

async function pick (movie) {
  if (!apiKey.value) return
  loadingPickId.value = movie.id
  try {
    // Dettagli + crediti
    const detailsUrl = new URL(`https://api.themoviedb.org/3/movie/${movie.id}`)
    detailsUrl.searchParams.set('api_key', apiKey.value)
    detailsUrl.searchParams.set('language', 'it-IT')
    detailsUrl.searchParams.set('append_to_response', 'credits')

    const details = await $fetch(detailsUrl.toString(), { headers: { accept: 'application/json' } })
    const director = details?.credits?.crew?.find(c => c.job === 'Director')?.name || null
    const cast = (details?.credits?.cast || []).slice(0, 5).map(c => c.name)

    const poster_url = details?.poster_path
      ? `https://image.tmdb.org/t/p/w500${details.poster_path}`
      : null

    const payload = {
      title: details?.title || movie.title,
      release_date: details?.release_date || movie.release_date || null,
      release_year: details?.release_date ? Number(details.release_date.slice(0,4)) : null,
      poster_url,
      director,
      cast,
      runtime: details?.runtime || null,
      tmdb_id: details?.id || movie.id
    }

    emit('prefill', payload)

    // 👇 CHIUDI LA LISTA + PULISCI LA RICERCA
    showResults.value = false
    results.value = []
    q.value = ''
    error.value = ''
    searched.value = false
  } catch (e) {
    console.error('[TMDb] details error:', e)
  } finally {
    loadingPickId.value = null
  }
}
</script>
