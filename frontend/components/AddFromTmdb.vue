<!-- components/AddFromTmdb.vue -->
<template>
  <ClientOnly>
    <div class="bg-white/5 border border-white/10 p-5 rounded-3xl shadow-xl backdrop-blur-md space-y-4">
      
      <!-- Header with Tabs & Close button -->
      <div class="flex items-center justify-between gap-4 border-b border-white/5 pb-3">
        <div class="flex items-center gap-3">
          <!-- Toggle search type -->
          <div class="inline-flex rounded-xl bg-white/5 border border-white/10 p-0.5" role="group">
            <button
              type="button"
              class="px-4 py-1.5 text-xs font-semibold cursor-pointer transition duration-150 rounded-l-xl"
              :class="searchType === 'movie'
                ? 'text-sky-300 bg-sky-500/10'
                : 'text-gray-400 hover:text-white'"
              @click="setType('movie')"
            >
              Film
            </button>
            <button
              type="button"
              class="px-4 py-1.5 text-xs font-semibold cursor-pointer transition duration-150 rounded-r-xl"
              :class="searchType === 'tv'
                ? 'text-purple-300 bg-purple-500/10'
                : 'text-gray-400 hover:text-white'"
              @click="setType('tv')"
            >
              Serie TV
            </button>
          </div>
        </div>

        <!-- Chiudi -->
        <button
          type="button"
          class="flex items-center justify-center w-8 h-8 text-gray-400 hover:text-white bg-white/5 border border-white/10 hover:bg-white/10 font-medium rounded-xl transition cursor-pointer shadow-sm"
          @click="close"
          title="Chiudi"
        >
          <svg class="w-4 h-4" aria-hidden="true" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Search bar input -->
      <div class="flex gap-2">
        <input
          v-model.trim="q"
          :placeholder="searchType === 'movie' ? 'Cerca un film da aggiungere...' : 'Cerca una serie TV da aggiungere...'"
          class="w-full bg-white/5 border border-white/10 text-white placeholder-gray-500 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all"
          @keyup.enter="doSearch(1)"
        />
        <button
          @click="doSearch(1)"
          class="px-5 py-2.5 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/40 text-purple-300 font-bold rounded-xl text-sm transition-all duration-150 cursor-pointer shadow-md shadow-purple-500/5"
        >
          Cerca
        </button>
      </div>

      <!-- States (Loading / Error / Empty) -->
      <ul v-if="loading" class="space-y-3">
        <SearchResultSkeleton v-for="n in 3" :key="n" />
      </ul>
      <div v-if="error" class="text-sm text-red-400 font-semibold text-left">Errore: {{ error }}</div>
      <div v-if="!loading && !error && searched && results.length === 0" class="text-sm text-gray-500 text-left">Nessun risultato trovato.</div>

      <!-- Results Grid list -->
      <ul
        v-if="showResults && results.length"
        ref="resultsTop"
        class="space-y-3"
      >
        <li
          v-for="r in results"
          :key="`${r.kind}-${r.id}`"
          class="py-4 px-4 flex items-start gap-4 rounded-2xl border border-white/5 bg-white/5 hover:bg-white/10 hover:border-white/10 transition-all duration-150"
        >
          <!-- Poster thumbnail -->
          <div class="w-16 h-24 bg-white/5 rounded-xl overflow-hidden flex-shrink-0 border border-white/5 shadow-sm">
            <img
              v-if="r.poster_url"
              :src="r.poster_url"
              class="w-full h-full object-cover"
              alt=""
              loading="lazy"
            />
            <div v-else class="w-full h-full flex items-center justify-center text-[10px] text-gray-500">
              N/A
            </div>
          </div>

          <!-- Description and actions -->
          <div class="min-w-0 flex-1 flex flex-col gap-2 text-left">
            <div>
              <div class="flex flex-wrap items-center gap-2">
                <span
                  class="inline-flex items-center rounded-md text-[9px] font-bold px-2 py-0.5"
                  :class="r.kind === 'movie'
                    ? 'bg-blue-500/20 border border-blue-500/30 text-blue-300'
                    : 'bg-yellow-500/20 border border-yellow-500/30 text-yellow-300'"
                >
                  {{ r.kind === 'movie' ? 'FILM' : 'SERIE' }}
                </span>

                <span class="font-bold text-white truncate text-sm">
                  {{ r.title }}
                </span>

                <span v-if="r.release_year" class="text-xs text-gray-400 font-medium">
                  ({{ r.release_year }})
                </span>

                <span v-if="r.vote_average" class="ml-auto flex items-center gap-0.5 text-xs font-semibold text-amber-400">
                  ★ {{ toFixed1(r.vote_average) }}
                </span>
              </div>

              <div class="text-xs text-gray-400 mt-1">
                <span class="text-gray-500 mr-1">Regia:</span>
                <span class="font-semibold text-white">
                  {{ r.director || '—' }}
                </span>
              </div>

              <p v-if="r.overview" class="text-xs text-gray-400 mt-2 line-clamp-2 leading-relaxed">
                {{ r.overview }}
              </p>
            </div>

            <!-- Actions block -->
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-end gap-2 mt-2 pt-2 border-t border-white/5">
              <!-- Add button -->
              <button
                @click="pick(r)"
                class="inline-flex items-center justify-center gap-1.5 text-xs font-bold px-4 py-2 rounded-xl bg-green-500/10 border border-green-500/20 text-green-300 hover:bg-green-500/20 disabled:opacity-60 w-full sm:w-auto cursor-pointer transition shadow-sm shadow-green-500/5"
                :disabled="loadingPickKey === `${r.kind}-${r.id}`"
              >
                <template v-if="loadingPickKey !== `${r.kind}-${r.id}`">
                  <svg class="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10 3a1 1 0 0 1 1 1v5h5a1 1 0 1 1 0 2h-5v5a1 1 0 1 1-2 0v-5H4a1 1 0 0 1 0-2h5V4a1 1 0 0 1 1-1Z"/>
                  </svg>
                  <span>Aggiungi</span>
                </template>
                <template v-else>
                  <svg class="animate-spin h-3.5 w-3.5" viewBox="0 0 24 24" fill="none">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4A4 4 0 008 12H4z"/>
                  </svg>
                  <span>Aggiungo…</span>
                </template>
              </button>

              <!-- Info link -->
              <a
                :href="`https://www.themoviedb.org/${r.kind === 'tv' ? 'tv' : 'movie'}/${r.tmdb_id}`"
                target="_blank"
                rel="noopener"
                class="inline-flex items-center justify-center gap-1.5 text-xs font-semibold px-4 py-2 rounded-xl border border-white/10 text-gray-300 bg-white/5 hover:bg-white/10 w-full sm:w-auto transition"
              >
                <svg class="w-3.5 h-3.5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M11 3h4.5A1.5 1.5 0 0117 4.5V9M9 11l7-7M9.5 3H5A2 2 0 003 5v10a2 2 0 002 2h10a2 2 0 002-2v-4.5"/>
                </svg>
                <span>TMDb Info</span>
              </a>
            </div>
          </div>
        </li>
      </ul>

      <!-- Pagination -->
      <div
        v-if="showResults && totalPages > 1"
        class="mt-4 flex items-center justify-center gap-3 select-none border-t border-white/5 pt-4"
      >
        <!-- Prev page -->
        <button
          type="button"
          class="inline-flex items-center gap-1 text-xs px-3.5 py-2 rounded-xl border border-white/10 text-gray-300 bg-white/5 hover:bg-white/10 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer transition shadow-sm"
          :disabled="page <= 1 || loading"
          @click="changePage(page - 1)"
        >
          <svg class="w-3.5 h-3.5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12.5 4.5L7.5 10l5 5.5"/>
          </svg>
          <span>Prec</span>
        </button>

        <!-- Page details -->
        <span class="text-xs text-gray-400 font-medium">
          Pagina {{ page }} / {{ totalPages }}
        </span>

        <!-- Next page -->
        <button
          type="button"
          class="inline-flex items-center gap-1 text-xs px-3.5 py-2 rounded-xl border border-white/10 text-gray-300 bg-white/5 hover:bg-white/10 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer transition shadow-sm"
          :disabled="page >= totalPages || loading"
          @click="changePage(page + 1)"
        >
          <span>Succ</span>
          <svg class="w-3.5 h-3.5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 4.5L12.5 10l-5 5.5"/>
          </svg>
        </button>
      </div>

    </div>
  </ClientOnly>
</template>

<script setup>
import SearchResultSkeleton from './SearchResultSkeleton.vue'
const emit = defineEmits(['added', 'close'])
const { apiFetch } = useApi()
const toast = useToast?.()

const q = ref('')
const searchType = ref('movie')

const results = ref([])
const loading = ref(false)
const error = ref('')
const searched = ref(false)
const resultsTop = ref(null)

const showResults = ref(false)
const loadingPickKey = ref(null)

const page = ref(1)
const totalPages = ref(1)

// Live Autocomplete Debounce Watcher
let debounceTimer = null
watch(q, (newVal) => {
  if (debounceTimer) clearTimeout(debounceTimer)
  
  const query = newVal.trim()
  if (query.length < 3) {
    if (query.length === 0) {
      results.value = []
      showResults.value = false
      searched.value = false
    }
    return
  }

  debounceTimer = setTimeout(() => {
    doSearch(1)
  }, 350) // 350ms delay
})

function toFixed1(v){ const n=Number(v); return Number.isFinite(n) ? n.toFixed(1) : v }

function setType(t) {
  if (t !== searchType.value) {
    searchType.value = t
    results.value = []
    showResults.value = false
    error.value = ''
    page.value = 1
    totalPages.value = 1
    if (q.value.trim().length >= 3) {
      doSearch(1)
    }
  }
}

function close() {
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

function scrollToResultsTop() {
  if (!resultsTop.value) return
  const rect = resultsTop.value.getBoundingClientRect()
  const top = rect.top + window.scrollY - 80
  window.scrollTo({ top, behavior: 'smooth' })
}

function changePage(newPage) {
  if (loading.value) return
  scrollToResultsTop()
  doSearch(newPage)
}

async function doSearch(goToPage = 1) {
  error.value = ''
  searched.value = true
  results.value = []
  showResults.value = false

  if (!q.value.trim()) {
    error.value = 'Inserisci un titolo'
    return
  }

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
  const key = `${item.kind}-${item.id}`
  loadingPickKey.value = key

  try {
    let details
    if (item.kind === 'movie') {
      details = await apiFetch(`/tmdb/details/${item.id}`)
    } else {
      details = await apiFetch(`/tmdb/tv/${item.id}`)
    }

    const body = {
      kind: details.kind || item.kind,
      title: details.title,
      status: 'to_watch',
      release_date: details.release_date || null,
      release_year: details.release_year ?? null,
      poster_url: details.poster_url || null,
      director: details.director || null,
      cast: Array.isArray(details.cast) ? details.cast : null,
      runtime: details.runtime ?? null,
      tmdb_id: details.tmdb_id || item.id,
      overview: details.overview || null,
      tmdb_vote: details.vote_average ?? item.vote_average ?? null,
    }

    const saved = await apiFetch('/movies/', {
      method: 'POST',
      body
    })

    emit('added', saved)
    toast?.show?.('success', `"${saved.title}" aggiunto alla tua lista`)
    close()
  } catch (e) {
    if (e?.response?.status === 409) {
      toast?.show?.('error', 'Questo titolo è già presente nella tua collezione!')
    } else {
      console.error('[TMDb] details/save error:', e)
      toast?.show?.('error', 'Errore durante aggiunta da TMDb')
    }
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
