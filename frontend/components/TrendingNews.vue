<template>
  <section class="bg-white text-black">
    <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
      <!-- <h2 class="text-md font-semibold">Novità & Tendenze</h2> -->

      <div class="flex flex-wrap items-center gap-2">
        <!-- Filtro media -->
        <div class="inline-flex rounded-md shadow-sm" role="group">
          <button
            v-for="(m, idx) in mediaTabs"
            :key="m.value"
            @click="media = m.value; refetch(true)"
            type="button"
            :class="[
              'px-4 py-2 text-sm font-medium border focus:z-10',
              idx === 0 ? 'rounded-s-lg' : idx === mediaTabs.length - 1 ? 'rounded-e-lg' : '',
              media === m.value
                ? 'text-white bg-blue-600 border-blue-600 focus:ring-2 focus:ring-blue-700'
                : 'text-gray-900 bg-white border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-800 dark:border-gray-700 dark:text-white dark:hover:text-white dark:hover:bg-gray-700 dark:focus:ring-blue-500 dark:focus:text-white'
            ]"
          >
            {{ m.label }}
          </button>
        </div>

        <!-- Finestra temporale -->
        <div class="inline-flex rounded-md shadow-sm" role="group">
          <button
            v-for="(w, idx) in windowTabs"
            :key="w.value"
            @click="windowVal = w.value; refetch(true)"
            type="button"
            :class="[
              'px-4 py-2 text-sm font-medium border focus:z-10',
              idx === 0 ? 'rounded-s-lg' : idx === windowTabs.length - 1 ? 'rounded-e-lg' : '',
              windowVal === w.value
                ? 'text-white bg-purple-600 border-purple-600 focus:ring-2 focus:ring-purple-700'
                : 'text-gray-900 bg-white border-gray-200 hover:bg-gray-100 hover:text-purple-700 focus:ring-2 focus:ring-purple-700 focus:text-purple-700 dark:bg-gray-800 dark:border-gray-700 dark:text-white dark:hover:text-white dark:hover:bg-gray-700 dark:focus:ring-purple-500 dark:focus:text-white'
            ]"
          >
            {{ w.label }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-sm opacity-70 py-4">Caricamento…</div>
    <div v-else-if="error" class="text-sm text-red-600">Errore: {{ error }}</div>
    <div v-else-if="items.length === 0" class="text-sm opacity-70">Nessun risultato.</div>

    <div class="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <article
        v-for="it in items"
        :key="`${it.kind}-${it.id}`"
        class="text-gray-800 rounded-lg  bg-white p-4 shadow-sm dark:border-gray-700 dark:bg-gray-800 w-full"
      >
        <div class="relative">
          <img
            v-if="it.poster_url"
            :src="it.poster_url"
            class="w-full aspect-[2/3] object-cover"
            loading="lazy"
          />
          <div v-else class="w-full aspect-[2/3] flex items-center justify-center text-xs text-gray-500 bg-gray-100">
            Nessun poster
          </div>

          <span
            class="absolute top-2 left-2 px-2 py-0.5 rounded text-xs font-medium shadow-sm"
            :class="it.kind==='tv'
              ? 'bg-yellow-100 text-yellow-800'
              : 'bg-blue-100 text-blue-800'"
          >
            {{ it.kind==='tv' ? 'SERIE' : 'FILM' }}
          </span>
        </div>

        <div class="p-3 space-y-2">
            <h3 class="text-md font-semibold leading-snug break-words text-black">
            <NuxtLink
              v-if="it.local_id"
              :to="it.kind==='tv' ? `/tv/${it.local_id}` : `/movies/${it.local_id}`"
              class="hover:underline"
            >
          {{ it.title.length > 25 ? it.title.slice(0, 25) + '...' : it.title }}
            </NuxtLink>
            <span v-else>{{ it.title.length > 25 ? it.title.slice(0, 25) + '...' : it.title }}</span>
          </h3>

          <p v-if="it.overview" class="text-xs text-gray-600 line-clamp-3">
            {{ it.overview }}
          </p>

           <p v-else class="text-xs text-gray-600 line-clamp-3">
            N/A
          </p>

          <div class="flex items-center justify-between text-xs text-gray-500">
            <span v-if="it.release_year">{{ it.release_year }}</span>
            <span v-if="it.vote_average">★ {{ toOne(it.vote_average) }}</span>
          </div>

          <!-- Azioni -->
           <div class="mt-4 flex items-center justify-between gap-4">
            <button
              class="text-green-700 hover:text-white border border-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 rounded-lg text-sm px-4 py-2 disabled:opacity-60"
              :disabled="addingKey === keyOf(it)"
              @click="quickAdd(it)"
              title="Aggiungi alla tua lista"
            >
              <span v-if="addingKey !== keyOf(it)">Aggiungi</span>
              <span v-else class="inline-flex items-center gap-1">
                <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4A4 4 0 008 12H4z"/>
                </svg>
                Salvo…
              </span>
            </button>

            <a type="button"
              :href="`https://www.themoviedb.org/${it.kind==='tv'?'tv':'movie'}/${it.tmdb_id}`"
              target="_blank" rel="noopener"
              class="text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700"
            >
              TMDB
            </a>
          </div>
        </div>
      </article>
    </div>

    <!-- Paginazione -->
    <div class="flex justify-center items-center gap-4 mt-6" v-if="totalPages > 1">
      <button
        type="button"
        class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 inline-flex items-center disabled:opacity-50 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
        :disabled="page <= 1 || loading"
        @click="goPrev()"
      >
        <svg class="w-3.5 h-3.5 me-2" aria-hidden="true" fill="none" viewBox="0 0 14 10">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5H1m0 0L5 9M1 5l4-4"/>
        </svg>
        Prec
      </button>

      <span class="text-sm opacity-70">Pagina {{ page }} / {{ totalPages }}</span>

      <button
        type="button"
        class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 inline-flex items-center disabled:opacity-50 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
        :disabled="page >= totalPages || loading"
        @click="goNext()"
      >
        Succ
        <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" fill="none" viewBox="0 0 14 10">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
      </button>
    </div>
  </section>
</template>

<script setup>
const { apiFetch } = useApi()
const toast = useToast?.() // se non hai un composable toast, sostituisci con alert

// Tabs
const mediaTabs = [
  { value: 'all',   label: 'Tutti' },
  { value: 'movie', label: 'Film' },
  { value: 'tv',    label: 'Serie' },
]
const windowTabs = [
  { value: 'day',  label: 'Oggi' },
  { value: 'week', label: 'Settimana' },
]

// Stato UI
const media = ref('all')
const windowVal = ref('day')
const page = ref(1)

const loading = ref(false)
const error = ref('')
const items = ref([])
const totalPages = ref(1)

const addingKey = ref(null)

// utils
function keyOf(it){ return `${it.kind}-${it.id}` }
function toOne(n){
  const x = typeof n === 'number' ? n : Number(n)
  return Number.isFinite(x) ? x.toFixed(1) : n
}

// fetch
async function refetch(resetPage = false) {
  if (resetPage) page.value = 1
  loading.value = true
  error.value = ''
  try {
    const data = await apiFetch('/tmdb/trending', {
      query: { media: media.value, window: windowVal.value, page: page.value, language: 'it-IT' }
    })
    // local_id ci servirà quando un elemento viene aggiunto al DB
    items.value = (data?.results || []).map(x => ({ ...x, local_id: x.local_id ?? null }))
    totalPages.value = data?.total_pages || 1
  } catch (e) {
    error.value = e?.data?.detail || e?.message || 'Errore'
  } finally {
    loading.value = false
  }
}
onMounted(() => refetch())

// Aggiunta rapida: prende i dettagli e salva nel DB
async function quickAdd(it) {
  addingKey.value = keyOf(it)
  try {
    const details = await apiFetch(it.kind === 'tv' ? `/tmdb/tv/${it.id}` : `/tmdb/details/${it.id}`)
    const body = {
      kind: details.kind || it.kind,
      title: details.title,
      status: 'to_watch',
      release_date: details.release_date || null,
      release_year: details.release_year ?? null,
      poster_url: details.poster_url || null,
      director: details.director || null,
      cast: Array.isArray(details.cast) ? details.cast : null,
      runtime: details.runtime ?? null,
      tmdb_id: details.tmdb_id || it.id,
      overview: details.overview || null
    }
    const saved = await apiFetch('/movies/', { method: 'POST', body })
    // aggiorna la card per linkarla alla tua pagina locale
    const idx = items.value.findIndex(x => keyOf(x) === keyOf(it))
    if (idx !== -1) items.value[idx].local_id = saved.id

    if (toast?.show) toast.show('success', `"${saved.title}" aggiunto!`)
    else alert(`"${saved.title}" aggiunto!`)
  } catch (e) {
    console.error('quickAdd trending error', e)
    if (toast?.show) toast.show('error', 'Errore durante aggiunta')
    else alert('Errore durante aggiunta')
  } finally {
    addingKey.value = null
  }
}


// scrolla la pagina in cima al contenuto del componente
function scrollToTopSmooth() {
  // se preferisci scrollare l'intera finestra:
  if (typeof window !== 'undefined') {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    return
  }
}

// cambia pagina indietro
async function goPrev() {
  if (page.value <= 1 || loading.value) return
  page.value = Math.max(1, page.value - 1)
  await refetch()
  scrollToTopSmooth()
}

// cambia pagina avanti
async function goNext() {
  if (page.value >= totalPages.value || loading.value) return
  page.value = Math.min(totalPages.value, page.value + 1)
  await refetch()
  scrollToTopSmooth()
}

</script>

<style scoped>

</style>
