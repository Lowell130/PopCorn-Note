<!-- pages/test.vue -->
<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h1 class="text-2xl font-semibold text-black">La tua Dashboard TEST</h1>
    </div>

    <!-- Toggle TMDb picker -->
    <div class="flex items-center justify-end mb-3">
      <button
        class="text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-4 py-2"
        @click="showPicker = !showPicker"
      >
        {{ showPicker ? 'Chiudi ricerca TMDb' : '+ Aggiungi da TMDb' }}
      </button>
    </div>

    <!-- TMDb picker + form -->
    <div class="gap-4 mb-6">
      <AddFromTmdb
        v-if="hasTmdb && showPicker"
        @prefill="onPrefill"
        @close="showPicker = false"
      />
      <AddMovieForm
        v-if="showForm"
        :initial-data="prefillData"
        @added="onAdded"
      />
    </div>

    <!-- Stats -->
    <DashboardStats :movies="movies" />

    <!-- Toolbar -->
    <div class="bg-white text-black rounded-xl p-3 shadow mb-4 flex flex-wrap gap-2">
      <input
        v-model="q"
        placeholder="Cerca titolo o nota…"
        class="flex-1 min-w-[200px] bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5"
      />

      <select
        v-model="kind"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg p-2.5"
        title="Tipo"
      >
        <option value="">Tutti</option>
        <option value="movie">Solo film</option>
        <option value="tv">Solo serie</option>
      </select>

      <select
        v-model="status"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg p-2.5"
      >
        <option value="">Tutti gli stati</option>
        <option value="to_watch">Da vedere</option>
        <option value="watched">Visto</option>
        <option value="upcoming">In uscita</option>
        <option value="watching">In visione</option>
      </select>

      <select
        v-model="sortBy"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg p-2.5"
      >
        <option value="created_at_desc">Recenti</option>
        <option value="title_asc">Titolo A→Z</option>
        <option value="score_desc">Score alto</option>
      </select>

      <button
        @click="resetFilters"
        class="text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5"
      >
        Reset
      </button>
    </div>

    <!-- Grid -->
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <MovieCard
        v-for="m in movies"
        :key="m.id"
        :movie="m"
        @updated="onUpdated"
        @deleted="onDeleted"
      />
    </div>

    <!-- Empty state -->
    <div v-if="!loading && movies.length === 0" class="text-center opacity-80 py-12">
      <div class="text-5xl mb-3">🍿</div>
      <div class="text-lg">Nessun film ancora. Aggiungine uno!</div>
    </div>

    <!-- Loader + sentinel -->
    <div ref="sentinel" class="h-10"></div>
    <div v-if="loading" class="text-sm opacity-70 py-4">Caricamento…</div>
    <div v-if="!hasMore && movies.length && !loading" class="text-center text-xs opacity-60 py-4">
      Fine elenco
    </div>
  </div>
</template>

<script setup>
import DashboardStats from '@/components/DashboardStats.vue'
import AddMovieForm from '@/components/AddMovieForm.vue'
import AddFromTmdb from '@/components/AddFromTmdb.vue'
import MovieCard from '@/components/MovieCard.vue'

definePageMeta({ layout: 'wide' })

const showPicker = ref(false)

const prefillData = ref(null)
function onPrefill(data) {
  prefillData.value = data
  showForm.value = true
}

const { apiFetch } = useApi()
const config = useRuntimeConfig()
const hasTmdb = computed(() => !!config.public.tmdbApiKey)

const movies = ref([])
const loading = ref(false)
const showForm = ref(false)

const q = ref('')
const status = ref('')
const sortBy = ref('created_at_desc')
const kind = ref('')

const limit = 20
let skip = 0
const hasMore = ref(true)
const sentinel = ref(null)
let observer

// ⬇️ ORDINAMENTO: "watching" in cima, poi il resto secondo sortBy
function sortClient(arr, key) {
  const a = [...arr]
  return a.sort((x, y) => {
    // priorità: in visione prima
    const px = x.status === 'watching' ? 0 : 1
    const py = y.status === 'watching' ? 0 : 1
    if (px !== py) return px - py

    // secondario: in base al sort selezionato
    if (key === 'title_asc') {
      return String(x.title || '').localeCompare(String(y.title || ''))
    }
    if (key === 'score_desc') {
      return (y.score || 0) - (x.score || 0)
    }
    // default: created_at_desc -> lascia l'ordine del backend (già per created_at desc)
    return 0
  })
}




// Fetch con query param server-side
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
    if (kind.value) params.set('kind', kind.value)

    // 👇 NUOVO: se non sto filtrando per status, priorizza "watching"
    if (!status.value) params.set('priority_status', 'watching')

    // 👇 SEMPRE: spingi i "Visto" in fondo
    params.set('push_last_status', 'watched')

    const page = await apiFetch(`/movies/?${params.toString()}`)

    // non serve più ri-ordinare sul client (puoi tenere la tua sortClient se vuoi)
    movies.value = reset ? page : [...movies.value, ...page]
    skip += page.length
    hasMore.value = page.length === limit
  } finally {
    loading.value = false
  }
}



// Watch filtri & ricerca → refetch
watch([q, status, sortBy, kind], () => fetchMovies({ reset: true }))

onMounted(() => {
  fetchMovies({ reset: true })
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
  kind.value = ''
  fetchMovies({ reset: true })
}

function onAdded(newMovie) {
  showForm.value = false
  movies.value = sortClient([newMovie, ...movies.value], sortBy.value)
}

function onUpdated(updatedMovie) {
  const idx = movies.value.findIndex(m => m.id === updatedMovie.id)
  if (idx !== -1) {
    const next = [...movies.value]
    next[idx] = updatedMovie
    movies.value = sortClient(next, sortBy.value)
  }
}

function onDeleted(id) {
  movies.value = movies.value.filter(m => m.id !== id)
}
</script>
