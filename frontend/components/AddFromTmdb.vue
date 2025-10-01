<!-- components/AddFromTmdb.vue -->
<template>
  <ClientOnly>
    <div class="bg-white text-black rounded-2xl p-5 shadow space-y-3">
      <!-- Header -->
      <div class="flex items-center justify-between gap-2">
        <h2 class="text-lg font-semibold">Aggiungi da TMDb</h2>

        <div class="flex items-center gap-2">
          <!-- Toggle tipo -->
          <div class="inline-flex rounded-md shadow-xs" role="group">
            <button
              type="button"
              class="px-4 py-2 text-sm font-medium border border-gray-200 rounded-s-lg focus:z-10 focus:ring-2 dark:border-gray-700"
              :class="searchType==='movie'
                ? 'text-white bg-blue-700 hover:bg-blue-800 focus:ring-blue-500 dark:bg-blue-600 dark:hover:bg-blue-700'
                : 'text-gray-900 bg-white hover:bg-gray-100 hover:text-blue-700 dark:bg-gray-800 dark:text-white dark:hover:bg-gray-700'"
              @click="setType('movie')"
            >Film</button>
            <button
              type="button"
              class="px-4 py-2 text-sm font-medium border border-gray-200 rounded-e-lg focus:z-10 focus:ring-2 dark:border-gray-700"
              :class="searchType==='tv'
                ? 'text-white bg-blue-700 hover:bg-blue-800 focus:ring-blue-500 dark:bg-blue-600 dark:hover:bg-blue-700'
                : 'text-gray-900 bg-white hover:bg-gray-100 hover:text-blue-700 dark:bg-gray-800 dark:text-white dark:hover:bg-gray-700'"
              @click="setType('tv')"
            >Serie</button>
          </div>

          <!-- Chiudi -->
          <button
            type="button"
class="flex items-center justify-center w-10 h-10 text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 font-medium rounded-full dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700"            @click="close"
            title="Chiudi"
          >
<svg class="w-[16px] h-[16px] text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18 17.94 6M18 18 6.06 6"/>
</svg>


          </button>
        </div>
      </div>

      <!-- Search -->
      <div class="flex gap-2">
        <input
          v-model.trim="q"
          :placeholder="searchType==='movie' ? 'Cerca film…' : 'Cerca serie…'"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-purple-500 focus:border-purple-500 block w-full p-2.5"
          @keyup.enter="doSearch(1)"
        />
        <button
          @click="doSearch(1)"
          class="focus:outline-none text-white bg-purple-700 hover:bg-purple-800 focus:ring-4 focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5"
        >
          Cerca
        </button>
      </div>

      <!-- Stati -->
      <div v-if="loading" class="text-sm opacity-70">Ricerca in corso…</div>
      <div v-if="error" class="text-sm text-red-600">Errore: {{ error }}</div>
      <div v-if="!loading && !error && searched && results.length === 0" class="text-sm opacity-70">Nessun risultato.</div>

      <!-- Risultati -->
      <ul v-if="showResults && results.length" class="divide-y">
        <li
          v-for="r in results"
          :key="`${r.kind}-${r.id}`"
          class="py-3 flex items-start gap-3"
        >
          <!-- poster -->
          <div class="w-16 h-24 bg-gray-100 rounded overflow-hidden flex-shrink-0">
            <img v-if="r.poster_url" :src="r.poster_url" class="w-full h-full object-cover" alt="" loading="lazy" />
          </div>

          <!-- testo -->
          <div class="min-w-0 flex-1">
            <div class="flex items-center gap-2">
              <span class="inline-flex items-center rounded-full text-[10px] px-2 py-0.5"
                    :class="r.kind==='movie' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'">
                {{ r.kind==='movie' ? 'FILM' : 'SERIE' }}
              </span>
              <span class="font-medium truncate">{{ r.title }}</span>
              <span v-if="r.release_year" class="text-xs text-gray-500">({{ r.release_year }})</span>
              <span v-if="r.vote_average" class="ml-1 text-xs text-amber-600">★ {{ toFixed1(r.vote_average) }}</span>
            </div>

            <div class="text-xs text-gray-600 mt-0.5">
              <span class="text-gray-500">Regia:</span>
              <span class="font-medium">{{ r.director || '—' }}</span>
            </div>

            <p v-if="r.overview" class="text-xs text-gray-600 mt-1 line-clamp-2">
              {{ r.overview }}
            </p>
          </div>

          <!-- azioni -->
          <div class="flex flex-col gap-2 items-end">
            <button
              @click="pick(r)"
              class="text-xs px-3 py-1.5 rounded bg-green-600 text-white disabled:opacity-60"
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

            <a
              :href="`https://www.themoviedb.org/${r.kind==='tv'?'tv':'movie'}/${r.tmdb_id}`"
              target="_blank" rel="noopener"
              class="text-xs px-3 py-1.5 rounded border"
            >
              TMDb
            </a>
          </div>
        </li>
      </ul>

      <!-- Paginazione -->
      <div v-if="showResults && totalPages>1" class="flex items-center justify-between pt-2">
        <button
          type="button"
          class="text-sm px-3 py-1.5 rounded border disabled:opacity-50"
          :disabled="page<=1 || loading"
          @click="doSearch(page-1)"
        >« Prec</button>

        <span class="text-xs opacity-70">Pagina {{ page }} / {{ totalPages }}</span>

        <button
          type="button"
          class="text-sm px-3 py-1.5 rounded border disabled:opacity-50"
          :disabled="page>=totalPages || loading"
          @click="doSearch(page+1)"
        >Succ »</button>
      </div>
    </div>
  </ClientOnly>
</template>

<script setup>
const emit = defineEmits(['prefill','close'])
const { apiFetch } = useApi()

const q = ref('')
const searchType = ref('movie') // 'movie' | 'tv'

const results = ref([])
const loading = ref(false)
const error = ref('')
const searched = ref(false)

const showResults = ref(false)
const loadingPickKey = ref(null)

const page = ref(1)
const totalPages = ref(1)

function toFixed1(v){ const n=Number(v); return Number.isFinite(n) ? n.toFixed(1) : v }

function setType(t) {
  if (t !== searchType.value) {
    searchType.value = t
    // reset
    results.value = []
    showResults.value = false
    error.value = ''
    page.value = 1
    totalPages.value = 1
  }
}

function close() {
  // pulizia + evento al genitore
  results.value = []
  q.value = ''
  error.value = ''
  searched.value = false
  showResults.value = false
  page.value = 1
  totalPages.value = 1
  emit('close')
}

onMounted(() => {
  const onKey = (e) => { if (e.key === 'Escape') close() }
  window.addEventListener('keydown', onKey)
  onUnmounted(() => window.removeEventListener('keydown', onKey))
})

async function doSearch(goToPage = 1) {
  error.value = ''
  searched.value = true
  results.value = []
  showResults.value = false

  if (!q.value.trim()) { error.value = 'Inserisci un titolo'; return }

  loading.value = true
  try {
    const data = await apiFetch('/tmdb/search', {
      query: { q: q.value.trim(), type: searchType.value, page: goToPage }
    })
    page.value = data?.page || goToPage
    totalPages.value = data?.total_pages || 1
    results.value = Array.isArray(data?.results) ? data.results : []
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
    // chiudo dopo la scelta
    close()
  } catch (e) {
    console.error('[TMDb] details error:', e)
  } finally {
    loadingPickKey.value = null
  }
}
</script>

<style scoped>
.line-clamp-2{
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;
}
</style>
