<!-- components/AddFromTmdb.vue -->
<template>
  <ClientOnly>
    <div class="bg-white text-black p-5 shadow space-y-3">
      <!-- Header -->
      <div class="flex items-center justify-between gap-2">
        <!-- <h2 class="text-lg font-semibold">Cerca ed aggiungi</h2> -->

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
class="flex items-center justify-center w-10 h-10 text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 font-medium rounded-full dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700 shadow-sm"            @click="close"
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
          class="shadow-sm focus:outline-none text-white bg-purple-700 hover:bg-purple-800 focus:ring-4 focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5"
        >
          Cerca
        </button>
      </div>

      <!-- Stati -->
      <div v-if="loading" class="text-sm opacity-70">Ricerca in corso…</div>
      <div v-if="error" class="text-sm text-red-600">Errore: {{ error }}</div>
      <div v-if="!loading && !error && searched && results.length === 0" class="text-sm opacity-70">Nessun risultato.</div>

    <!-- Risultati -->
<ul
  v-if="showResults && results.length"
   ref="resultsTop"
  class="space-y-3"
>
  <li
    v-for="r in results"
    :key="`${r.kind}-${r.id}`"
    class="py-3 px-3 flex items-start gap-3 rounded-lg border border-gray-100 bg-white hover:bg-purple-50/40 hover:border-purple-200 transition-colors"
  >
    <!-- poster -->
    <div class="w-16 h-24 bg-gray-100 rounded overflow-hidden flex-shrink-0">
      <img
        v-if="r.poster_url"
        :src="r.poster_url"
        class="w-full h-full object-cover"
        alt=""
        loading="lazy"
      />
      <div v-else class="w-full h-full flex items-center justify-center text-[10px] text-gray-400">
        N/A
      </div>
    </div>

    <!-- testo + azioni -->
    <div class="min-w-0 flex-1 flex flex-col gap-2">
      <!-- titolo + meta -->
      <div>
        <div class="flex flex-wrap items-center gap-2">
          <span
            class="inline-flex items-center rounded-full text-[10px] px-2 py-0.5"
            :class="r.kind==='movie'
              ? 'bg-blue-100 text-blue-700'
              : 'bg-green-100 text-green-700'"
          >
            {{ r.kind==='movie' ? 'FILM' : 'SERIE' }}
          </span>

          <span class="font-medium truncate text-sm">
            {{ r.title }}
          </span>

          <span
            v-if="r.release_year"
            class="text-[11px] text-gray-500"
          >
            ({{ r.release_year }})
          </span>

          <span
            v-if="r.vote_average"
            class="ml-auto flex items-center gap-1 text-[11px] text-amber-600"
          >
            <svg class="w-3 h-3" viewBox="0 0 20 20" fill="currentColor">
              <path
                d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 0 0 .95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.802 2.037a1 1 0 0 0-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118L10 13.347l-2.975 2.137c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 0 0-.364-1.118L3.39 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 0 0 .95-.69l1.07-3.292Z"
              />
            </svg>
            {{ toFixed1(r.vote_average) }}
          </span>
        </div>

        <div class="text-[11px] text-gray-600 mt-0.5">
          <span class="text-gray-500">Regia:</span>
          <span class="font-medium">
            {{ r.director || '—' }}
          </span>
        </div>

        <p
          v-if="r.overview"
          class="text-xs text-gray-600 mt-1 line-clamp-2"
        >
          {{ r.overview }}
        </p>
      </div>

      <!-- azioni -->
      <div
        class="flex flex-col sm:flex-row sm:items-center sm:justify-end gap-2 mt-1"
      >
        <!-- Aggiungi -->
        <button
          @click="pick(r)"
          class="inline-flex items-center justify-center gap-1.5 text-xs px-3 py-1.5 rounded-full bg-emerald-600 text-white hover:bg-emerald-700 disabled:opacity-60 w-full sm:w-auto"
          :disabled="loadingPickKey === `${r.kind}-${r.id}`"
        >
          <template v-if="loadingPickKey !== `${r.kind}-${r.id}`">
            <svg
              class="w-3.5 h-3.5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                d="M10 3a1 1 0 0 1 1 1v5h5a1 1 0 1 1 0 2h-5v5a1 1 0 1 1-2 0v-5H4a1 1 0 0 1 0-2h5V4a1 1 0 0 1 1-1Z"
              />
            </svg>
            <span>Aggiungi</span>
          </template>
          <template v-else>
            <svg class="animate-spin h-3.5 w-3.5" viewBox="0 0 24 24" fill="none">
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              />
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v4A4 4 0 008 12H4z"
              />
            </svg>
            <span>Prendo…</span>
          </template>
        </button>

        <!-- Info su TMDb -->
        <a
          :href="`https://www.themoviedb.org/${r.kind==='tv'?'tv':'movie'}/${r.tmdb_id}`"
          target="_blank"
          rel="noopener"
          class="inline-flex items-center justify-center gap-1.5 text-xs px-3 py-1.5 rounded-full border border-gray-300 text-gray-700 hover:bg-gray-100 w-full sm:w-auto"
        >
          <svg
            class="w-3.5 h-3.5"
            viewBox="0 0 20 20"
            fill="none"
          >
            <path
              d="M11 3h4.5A1.5 1.5 0 0 1 17 4.5V9"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <path
              d="M9 11l7-7"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <path
              d="M9.5 3H5A2 2 0 0 0 3 5v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-4.5"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          <span>Info</span>
        </a>
      </div>
    </div>
  </li>
</ul>


      <!-- Paginazione -->
     <!-- Paginazione -->
<div
  v-if="showResults && totalPages > 1"
  class="mt-4 flex items-center justify-center gap-3"
>
  <!-- Prec -->
<button
  type="button"
  class="inline-flex items-center gap-1 text-xs px-3 py-1.5 rounded-full border border-gray-300 text-gray-700 hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed"
  :disabled="page <= 1 || loading"
  @click="changePage(page - 1)"
>
    <svg class="w-3 h-3" viewBox="0 0 20 20" fill="none">
      <path
        d="M12.5 4.5 7.5 10l5 5.5"
        stroke="currentColor"
        stroke-width="1.7"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
    </svg>
    <span>Prec</span>
  </button>

  <!-- Info pagina -->
  <span class="text-xs text-gray-500">
    Pagina {{ page }} / {{ totalPages }}
  </span>

  <!-- Succ -->
<button
  type="button"
  class="inline-flex items-center gap-1 text-xs px-3 py-1.5 rounded-full border border-gray-300 text-gray-700 hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed"
  :disabled="page >= totalPages || loading"
  @click="changePage(page + 1)"
>
    <span>Succ</span>
    <svg class="w-3 h-3" viewBox="0 0 20 20" fill="none">
      <path
        d="M7.5 4.5 12.5 10l-5 5.5"
        stroke="currentColor"
        stroke-width="1.7"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
    </svg>
  </button>
</div>

    </div>
  </ClientOnly>
</template>

<script setup>
const emit = defineEmits(['added', 'close'])
const { apiFetch } = useApi()
const toast = useToast?.()

const q = ref('')
const searchType = ref('movie') // 'movie' | 'tv'

const results = ref([])
const loading = ref(false)
const error = ref('')
const searched = ref(false)
const resultsTop = ref(null)

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


function scrollToResultsTop() {
  if (!resultsTop.value) return
  const rect = resultsTop.value.getBoundingClientRect()
  const top = rect.top + window.scrollY - 80 // offset per header / margine
  window.scrollTo({ top, behavior: 'smooth' })
}

function changePage(newPage) {
  if (loading.value) return
  // fai lo scroll SUBITO
  scrollToResultsTop()
  // poi lancia la ricerca sulla nuova pagina
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
    // 1. Recupero dettagli completi da TMDb
    let details
    if (item.kind === 'movie') {
      details = await apiFetch(`/tmdb/details/${item.id}`)
    } else {
      details = await apiFetch(`/tmdb/tv/${item.id}`)
    }

    // 2. Costruisco il payload per il backend
    const body = {
      kind: details.kind || item.kind,
      title: details.title,
      status: 'to_watch', // default sensato
      release_date: details.release_date || null,
      release_year: details.release_year ?? null,
      poster_url: details.poster_url || null,
      director: details.director || null,
      cast: Array.isArray(details.cast) ? details.cast : null,
      runtime: details.runtime ?? null,
      tmdb_id: details.tmdb_id || item.id,
      overview: details.overview || null,
      tmdb_vote: details.vote_average ?? item.vote_average ?? null,  // 👈 AGGIUNTO
    }

    // 3. Salvo direttamente nel DB
    const saved = await apiFetch('/movies/', {
      method: 'POST',
      body
    })

    // 4. Notifico il padre + toast
    emit('added', saved)
    toast?.show?.('success', `"${saved.title}" aggiunto alla tua lista`)
    // chiudo il picker
    close()
  } catch (e) {
    console.error('[TMDb] details/save error:', e)
    if (e?.response?.status === 409) {
      toast?.show?.('error', 'Questo titolo è già presente nella tua collezione!')
    } else {
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
