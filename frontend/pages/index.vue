<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h1 class="text-2xl font-semibold text-black">La tua Dashboard</h1>
      <!-- <div class="flex gap-2">
        <button
          class="text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-4 py-2"
          @click="showForm = !showForm"
        >
          + Aggiungi film
        </button>
      </div> -->
    </div>

    <!-- Barra strumenti -->
    <!-- <div class="bg-white text-black rounded-xl p-3 shadow mb-4 flex flex-wrap gap-2">
      <input v-model="q" placeholder="Cerca titolo o nota…" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" />
      <select v-model="status" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
        <option value="">Tutti</option>
        <option value="to_watch">Da vedere</option>
        <option value="watched">Visto</option>
        <option value="upcoming">In uscita</option>
      </select>
      <select v-model="sortBy" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
        <option value="created_at_desc">Recenti</option>
        <option value="title_asc">Titolo A→Z</option>
        <option value="score_desc">Score alto</option>
      </select>
      <button @click="resetFilters" class="focus:outline-none text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900">Reset</button>
    </div> -->

  

<!-- TMDb picker + form -->
<div class="gap-4 mb-6">
  <AddFromTmdb v-if="hasTmdb" @prefill="onPrefill" />
  <AddMovieForm v-if="showForm" :initial-data="prefillData" @added="onAdded" />
</div>

    <!-- Stats -->
    <DashboardStats :movies="movies" />
    <!-- Barra strumenti -->
<div class="bg-white text-black rounded-xl p-3 shadow mb-4 flex flex-wrap gap-2">
  <!-- Campo di ricerca: occupa tutto lo spazio -->
  <input
    v-model="q"
    placeholder="Cerca titolo o nota…"
    class="flex-1 min-w-[200px] bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
  />

  <!-- 🔽 Filtro tipo -->
  <select
    v-model="kind"
    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    title="Tipo"
  >
    <option value="">Tutti</option>
    <option value="movie">Solo film</option>
    <option value="tv">Solo serie</option>
  </select>

  <!-- Stato -->
  <select
    v-model="status"
    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
  >
    <option value="">Tutti gli stati</option>
    <option value="to_watch">Da vedere</option>
    <option value="watched">Visto</option>
    <option value="upcoming">In uscita</option>
    <option value="watching">In visione</option>
  </select>

  <!-- Ordinamento -->
  <select
    v-model="sortBy"
    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
  >
    <option value="created_at_desc">Recenti</option>
    <option value="title_asc">Titolo A→Z</option>
    <option value="score_desc">Score alto</option>
  </select>

  <!-- Reset -->
  <button
    @click="resetFilters"
    class="focus:outline-none text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900"
  >
    Reset
  </button>
</div>


<!-- pages/index.vue -->
<MovieRowCard
  v-for="m in movies"
  :key="m.id"
  :movie="m"
  @updated="onUpdated"
  @deleted="onDeleted"
/>
  
    <!-- Empty state -->
    <div v-if="!loading && movies.length === 0" class="text-center opacity-80 py-12">
      <div class="text-5xl mb-3">🍿</div>
      <div class="text-lg">Nessun film ancora. Aggiungine uno!</div>
    </div>

    

    <!-- Lista -->
    <!-- <div v-else class="grid md:grid-cols-2 gap-4">
      <MovieCard
        v-for="m in movies"
        :key="m.id"
        :movie="m"
        @updated="onUpdated"
        @deleted="onDeleted"
      />
    </div> -->

    <!-- Loader + sentinel per infinite scroll -->
    <div ref="sentinel" class="h-10"></div>
    <div v-if="loading" class="text-sm opacity-70 py-4">Caricamento…</div>
    <div v-if="!hasMore && movies.length && !loading" class="text-center text-xs opacity-60 py-4">
      Fine elenco
    </div>

  <!-- (1) NUOVO: Film in uscita da TMDb -->
    <!-- <UpcomingMovies
      class="mb-6"
      :months="3"
      region="IT"
      language="it-IT"
      @prefill="onPrefill"
    />
    -->

  </div>

  
</template>

<script setup>
import DashboardStats from '@/components/DashboardStats.vue'
import AddMovieForm from '@/components/AddMovieForm.vue'
import AddFromTmdb from '@/components/AddFromTmdb.vue'
import MovieCard from '@/components/MovieCard.vue'
import UpcomingMovies from '@/components/UpcomingMovies.vue'  // (2) NUOVO import



const prefillData = ref(null)
function onPrefill(data) {
  prefillData.value = data
  showForm.value = true
}

const { apiFetch } = useApi()
const config = useRuntimeConfig()
const hasTmdb = computed(()=> !!config.public.tmdbApiKey)

const movies = ref([])
const loading = ref(false)
const showForm = ref(false)

const q = ref('')
const status = ref('')
const sortBy = ref('created_at_desc')
const kind = ref('') // 🔽 NUOVO: '' | 'movie' | 'tv'

const limit = 20
let skip = 0
const hasMore = ref(true)
const sentinel = ref(null)
let observer

// Fetch con query param server-side
async function fetchMovies({ reset = false } = {}) {
  if (loading.value) return
  loading.value = true
  try {
    if (reset) {
      skip = 0
      movies.value = []
      hasMore.value = true
    }
    const params = new URLSearchParams()
    params.set('limit', String(limit))
    params.set('skip', String(skip))
    if (status.value) params.set('status', status.value)
    if (q.value.trim()) params.set('q', q.value.trim())
    if (kind.value) params.set('kind', kind.value) // 🔽 NUOVO

    // ordinamento: backend già sort per created_at desc; per altri tipi gestiamo client-side dopo
    const page = await apiFetch(`/movies/?${params.toString()}`)
    // sort client-side aggiuntivo
    const sorted = sortClient(page, sortBy.value)

    movies.value = reset ? sorted : [...movies.value, ...sorted]
    skip += page.length
    hasMore.value = page.length === limit
  } finally {
    loading.value = false
  }
}

function sortClient(arr, key) {
  const a = [...arr]
  if (key === 'title_asc') a.sort((x,y)=> String(x.title).localeCompare(String(y.title)))
  if (key === 'score_desc') a.sort((x,y)=> (y.score||0) - (x.score||0))
  // created_at_desc: già ok dal backend (fallback)
  return a
}

// Watch filtri & ricerca → refetch
watch([q, status, sortBy, kind], () => fetchMovies({ reset: true })) // 🔽 aggiunto kind

onMounted(() => {
  fetchMovies({ reset: true })
  // IntersectionObserver per infinite scroll
  observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && hasMore.value && !loading.value) {
      fetchMovies()
    }
  })
  if (sentinel.value) observer.observe(sentinel.value)
})

onBeforeUnmount(() => {
  if (observer && sentinel.value) observer.unobserve(sentinel.value)
})

function resetFilters() {
  q.value = ''
  status.value = ''
  sortBy.value = 'created_at_desc'
    kind.value = ''              // 🔽 reset tipo
 
}

function onAdded(newMovie) {
  showForm.value = false
  // prepend (rispetta ordine recenti)
  movies.value.unshift(newMovie)
}

function onUpdated(updatedMovie) {
  const idx = movies.value.findIndex(m => m.id === updatedMovie.id)
  if (idx !== -1) movies.value[idx] = updatedMovie
}

function onDeleted(id) {
  movies.value = movies.value.filter(m => m.id !== id)
}

const prefillTitle = ref('')
function prefillFromTmdb(title) {
  prefillTitle.value = title
  showForm.value = true
}
</script>
