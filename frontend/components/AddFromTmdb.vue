<!-- components/AddFromTmdb.vue -->
<template>
  <ClientOnly>
    <div class="bg-white text-black rounded-2xl p-5 shadow space-y-3">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-semibold">Aggiungi</h2>

       <!-- Toggle tipo -->
<!-- Toggle tipo -->
<div class="inline-flex rounded-md shadow-xs" role="group">
  <!-- Film -->
  <button
    type="button"
    class="px-4 py-2 text-sm font-medium border border-gray-200 rounded-s-lg focus:z-10 focus:ring-2 dark:border-gray-700"
    :class="searchType==='movie'
      ? 'text-white bg-blue-700 hover:bg-blue-800 focus:ring-blue-500 dark:bg-blue-600 dark:hover:bg-blue-700'
      : 'text-gray-900 bg-white hover:bg-gray-100 hover:text-blue-700 dark:bg-gray-800 dark:text-white dark:hover:bg-gray-700'"
    @click="setType('movie')"
  >
    Film
  </button>

  <!-- Serie -->
  <button
    type="button"
    class="px-4 py-2 text-sm font-medium border border-gray-200 rounded-e-lg focus:z-10 focus:ring-2 dark:border-gray-700"
    :class="searchType==='tv'
      ? 'text-white bg-blue-700 hover:bg-blue-800 focus:ring-blue-500 dark:bg-blue-600 dark:hover:bg-blue-700'
      : 'text-gray-900 bg-white hover:bg-gray-100 hover:text-blue-700 dark:bg-gray-800 dark:text-white dark:hover:bg-gray-700'"
    @click="setType('tv')"
  >
    Serie
  </button>
</div>


      </div>

      <div class="flex gap-2">
        <input
          v-model.trim="q"
          :placeholder="searchType==='movie' ? 'Cerca film...' : 'Cerca serie...'"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-purple-500 focus:border-purple-500 block w-full p-2.5"
          @keyup.enter="search"
        />
        <button
          @click="search"
          class="focus:outline-none text-white bg-purple-700 hover:bg-purple-800 focus:ring-4 focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5"
        >
          Cerca
        </button>
      </div>

      <div v-if="loading" class="text-sm opacity-70">Ricerca in corso…</div>
      <div v-if="error" class="text-sm text-red-600">Errore: {{ error }}</div>
      <div v-if="!loading && !error && searched && results.length === 0" class="text-sm opacity-70">
        Nessun risultato.
      </div>

      <ul v-if="showResults && results.length" class="divide-y">
        <li
          v-for="r in results"
          :key="`${r.kind}-${r.id}`"
          class="py-2 flex items-center justify-between"
        >
          <div class="min-w-0">
            <div class="font-medium truncate flex items-center gap-2">
              <span class="inline-flex items-center rounded-full text-xs px-2 py-0.5"
                    :class="r.kind==='movie' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'">
                {{ r.kind==='movie' ? 'FILM' : 'SERIE' }}
              </span>
              <span class="truncate">{{ r.title }}</span>
            </div>
            <div class="text-xs opacity-70">{{ r.release_date || '—' }}</div>
          </div>

          <button
            @click="pick(r)"
            class="text-sm px-3 py-1 rounded bg-green-600 text-white disabled:opacity-60"
            :disabled="loadingPickKey === `${r.kind}-${r.id}`"
          >
            <span v-if="loadingPickKey !== `${r.kind}-${r.id}`">Usa dati</span>
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
const { apiFetch } = useApi()

const q = ref('')
const searchType = ref('movie') // 'movie' | 'tv'

const results = ref([])
const loading = ref(false)
const error = ref('')
const searched = ref(false)

const showResults = ref(false)
const loadingPickKey = ref(null)

function setType(t) {
  if (t !== searchType.value) {
    searchType.value = t
    // reset lista quando cambio tipo
    results.value = []
    showResults.value = false
    error.value = ''
  }
}

async function search () {
  error.value = ''
  searched.value = true
  results.value = []
  showResults.value = false

  if (!q.value.trim()) { error.value = 'Inserisci un titolo'; return }

  loading.value = true
  try {
    const res = await apiFetch('/tmdb/search', { query: { q: q.value.trim(), type: searchType.value } })
    results.value = Array.isArray(res) ? res : []
    showResults.value = results.value.length > 0
  } catch (e) {
    console.error('[TMDb] search error:', e)
    error.value = e?.response?._data?.detail || e?.message || 'Errore sconosciuto'
  } finally {
    loading.value = false
  }
}

async function pick (item) {
  loadingPickKey.value = `${item.kind}-${item.id}`
  try {
    let details
    if (item.kind === 'movie') {
      details = await apiFetch(`/tmdb/details/${item.id}`)
    } else {
      details = await apiFetch(`/tmdb/tv/${item.id}`)
    }

    // Il backend restituisce già i campi normalizzati (title, release_date, release_year, poster_url, overview, cast, runtime, director, tmdb_id) + kind
    const payload = {
      kind: details.kind || item.kind,
      title: details.title,
      release_date: details.release_date || null,
      release_year: details.release_year ?? null,
      poster_url: details.poster_url || null,
      director: details.director || null,
      cast: Array.isArray(details.cast) ? details.cast : null,
      runtime: details.runtime ?? null,
      tmdb_id: details.tmdb_id || item.id,
      overview: details.overview || null
    }

    emit('prefill', payload)

    // chiudi e pulisci
    showResults.value = false
    results.value = []
    q.value = ''
    error.value = ''
    searched.value = false
  } catch (e) {
    console.error('[TMDb] details error:', e)
  } finally {
    loadingPickKey.value = null
  }
}
</script>
