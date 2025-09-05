<template>
  <section class="bg-white  rounded-2xl p-5 shadow text-black">
    <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
      <h2 class="text-xl font-semibold">Novità & Tendenze</h2>

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
      // primi/ultimi pulsanti con bordi arrotondati
      idx === 0 ? 'rounded-s-lg' : idx === mediaTabs.length - 1 ? 'rounded-e-lg' : '',
      // stile se attivo
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
      // bordi arrotondati a inizio/fine gruppo
      idx === 0 ? 'rounded-s-lg' : idx === windowTabs.length - 1 ? 'rounded-e-lg' : '',
      // attivo vs inattivo
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

    <div v-if="loading" class="text-sm opacity-70">Caricamento…</div>
    <div v-else-if="error" class="text-sm text-red-600">Errore: {{ error }}</div>
    <div v-else-if="items.length === 0" class="text-sm opacity-70">Nessun risultato.</div>

    <div class="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <article
        v-for="it in items"
        :key="`${it.kind}-${it.id}`"
        class="border rounded-lg overflow-hidden bg-white  shadow-sm"
      >
        <div class="relative">
          <img
            v-if="it.poster_url"
            :src="it.poster_url"
            class="w-full aspect-[2/3] object-cover"
            loading="lazy"
          />
          <div v-else class="w-full aspect-[2/3] flex items-center justify-center text-xs text-gray-500 bg-gray-100 ">
            Nessun poster
          </div>

          <span
            class="absolute top-2 left-2 px-2 py-0.5 rounded text-xs font-medium"
            :class="it.kind==='tv'
              ? 'bg-yellow-100 text-yellow-800'
              : 'bg-blue-100 text-blue-800'"
          >
            {{ it.kind==='tv' ? 'SERIE' : 'FILM' }}
          </span>
        </div>

        <div class="p-3 space-y-2">
          <h3 class="text-sm font-semibold leading-tight line-clamp-2 text-black">
            <NuxtLink
              :to="it.kind==='tv' ? `/tv/${linkId(it)}` : `/movies/${linkId(it)}`"
              class="hover:underline"
              v-if="it.local_id"
            >
              {{ it.title }}
            </NuxtLink>
            <span v-else>{{ it.title }}</span>
          </h3>

          <p v-if="it.overview" class="text-xs text-gray-600 line-clamp-3">
            {{ it.overview }}
          </p>

          <div class="flex items-center justify-between text-xs text-gray-500">
            <span v-if="it.release_year">{{ it.release_year }}</span>
            <span v-if="it.vote_average">★ {{ it.vote_average?.toFixed?.(1) ?? it.vote_average }}</span>
          </div>

        
        <!-- Azioni -->
    <div class="flex gap-2">
      <button
        class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
        @click="prefill(it)"
        title="Aggiungi alla tua lista"
      >
        Aggiungi
        <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
      </button>

      <a
        :href="`https://www.themoviedb.org/${it.kind==='tv'?'tv':'movie'}/${it.tmdb_id}`"
        target="_blank" rel="noopener"
        class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-gray-700 rounded-lg hover:bg-gray-800 focus:ring-4 focus:outline-none focus:ring-gray-300 dark:bg-gray-600 dark:hover:bg-gray-700 dark:focus:ring-gray-800"
      >
        TMDb
      </a>
          </div>
        </div>
      </article>
    </div>

   <!-- Paginazione con stile migliorato -->
<div class="flex justify-center items-center gap-4 mt-6" v-if="totalPages > 1">
  <!-- Bottone precedente -->
  <button
    type="button"
    class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center disabled:opacity-50 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
    :disabled="page <= 1 || loading"
    @click="page--; refetch()"
  >
    <svg class="w-3.5 h-3.5 me-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
      <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5H1m0 0L5 9M1 5l4-4"/>
    </svg>
    Prec
  </button>

  <!-- Info pagina -->
  <span class="text-sm opacity-70">Pagina {{ page }} / {{ totalPages }}</span>

  <!-- Bottone successivo -->
  <button
    type="button"
    class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center disabled:opacity-50 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
    :disabled="page >= totalPages || loading"
    @click="page++; refetch()"
  >
    Succ
    <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
      <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
    </svg>
  </button>
</div>
  </section>
</template>

<script setup>
const emit = defineEmits(['prefill']) // per aprire AddMovieForm con dati precompilati
const { apiFetch } = useApi()

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

// fetch
async function refetch(resetPage = false) {
  if (resetPage) page.value = 1
  loading.value = true
  error.value = ''
  try {
    const data = await apiFetch('/tmdb/trending', {
      query: { media: media.value, window: windowVal.value, page: page.value, language: 'it-IT' }
    })
    items.value = (data?.results || []).map(x => ({ ...x, local_id: null })) // local_id lo useremo se già presente in DB
    totalPages.value = data?.total_pages || 1
  } catch (e) {
    error.value = e?.data?.detail || e?.message || 'Errore'
  } finally {
    loading.value = false
  }
}
onMounted(() => refetch())

// helper: restituisce id locale se in futuro vuoi collegare con i record già salvati
function linkId(it) {
  return it.local_id || it.id
}

// prefill per AddMovieForm
function prefill(it) {
  emit('prefill', {
    title: it.title,
    release_date: it.release_date || null,
    release_year: it.release_year || null,
    poster_url: it.poster_url || null,
    overview: it.overview || null,
    director: null,
    cast: [],
    runtime: null,
    tmdb_id: it.tmdb_id || it.id,
    kind: it.kind || 'movie',
  })
}
</script>

<style scoped>
.line-clamp-2{
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;
}
.line-clamp-3{
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;
}
</style>
