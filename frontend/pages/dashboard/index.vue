<!-- pages/index.vue -->
<template>
  <div>
     <span v-if="user" class="text-gray-500 text-left font-normal">Ciao, <span class="font-semibold text-transparent bg-clip-text bg-gradient-to-r to-emerald-600 from-sky-400">{{ user.username || user.email }}</span>, ecco
        </span>
    <div>
      <h1 class="text-2xl font-semibold text-black mb-6">la tua Dashboard</h1>
      
    </div>

<!-- Action Bar -->
<div class="mb-4 flex gap-3">
  <button
    @click="showPicker = !showPicker"
    class="flex-1 flex items-center justify-between gap-4 px-5 py-3 text-white bg-gradient-to-r from-emerald-600 to-green-500 hover:from-emerald-700 hover:to-green-600 focus:outline-none focus:ring-4 focus:ring-green-300 dark:focus:ring-green-800 rounded-lg shadow-md transition-all"
  >
    <!-- Left side -->
    <div class="flex items-center gap-3">
      <div class="h-9 w-9 flex items-center justify-center rounded-full bg-white/20 border border-white/30 text-lg">
        🎬
      </div>
      <span class="text-sm sm:text-base font-medium">
        {{ showPicker ? 'Chiudi ricerca' : 'Aggiungi Film o Serie TV' }}
      </span>
    </div>

    <!-- Right side -->
    <div class="flex items-center gap-2 text-xs sm:text-sm opacity-90">
      <span class="hidden sm:inline">Dati completi da TMDb</span>
      <svg
        class="w-4 h-4 transform transition-transform duration-300"
        :class="showPicker ? 'rotate-180' : ''"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <path
          d="M6 9l6 6 6-6"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </div>
  </button>
  
  <!-- Random Picker Button -->
   <button
    @click="showRandomPicker = true"
    class="flex-shrink-0 flex items-center justify-center gap-2 px-5 py-3 text-white bg-gradient-to-r from-purple-600 to-pink-500 hover:from-purple-700 hover:to-pink-600 focus:outline-none focus:ring-4 focus:ring-purple-300 rounded-lg shadow-md transition-all sm:w-auto"
    title="Cosa guardo stasera?"
  >
    <span class="text-xl">🎲</span>
    <span class="hidden sm:inline font-medium">Fai scegliere al fato</span>
  </button>
</div>

<!-- Random Picker Modal -->
<Transition name="fade-slide">
  <RandomPickerModal v-if="showRandomPicker" @close="showRandomPicker = false" />
</Transition>



    <!-- TMDb picker + form -->
  <!-- TMDb picker + form (con transizione) -->
<Transition name="fade-slide" mode="out-in">
  <div v-if="hasTmdb && showPicker" class="mb-6">
    <AddFromTmdb
      @added="onAddedFromTmdb"
      @close="showPicker = false"
    />
  </div>
</Transition>

   


    <!-- Layout: sidebar filtri + griglia card -->
    <div class="mt-6 lg:grid lg:grid-cols-4 lg:gap-4">





  <!-- Griglia -->
  <!-- Griglia -->
  <div class="lg:col-span-3">
    <!-- Bottone drawer (solo mobile, SOPRA la griglia) -->
   <div class="mb-4 flex justify-end lg:hidden">
  <button
    @click="isFiltersOpen = true"
    class="w-full inline-flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-white bg-gray-800 rounded-lg hover:bg-gray-700 focus:outline-none lg:w-auto"
  >
    🎛️
    <span>Filtri</span>
  </button>
</div>

    <!-- Griglia card -->
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3">
      <MovieCard
        v-for="m in movies"
        :key="m.id"
        :movie="m"
        @updated="onUpdated"
        @deleted="onDeleted"
      />
      <!-- Skeletons -->
       <template v-if="loading">
         <MovieCardSkeleton v-for="n in (movies.length ? 3 : 6)" :key="'skel-'+n" />
       </template>
    </div>



<!-- Drawer sidebar per mobile -->
<!-- Drawer sidebar per mobile (gestito da Vue) -->
<Transition name="drawer-slide">
  <div
    v-if="isFiltersOpen"
    class="fixed inset-0 z-40 flex lg:hidden"
  >
    <!-- Backdrop -->
    <div
      class="fixed inset-0 bg-black/40"
      @click="isFiltersOpen = false"
    ></div>

    <!-- Pannello -->
    <div
      class="relative h-full w-80 bg-white dark:bg-gray-800 p-4 overflow-y-auto shadow-lg drawer-scroll"
    >
      <div class="flex items-center justify-between mb-4">
        <h5 class="text-base font-semibold text-gray-500 uppercase dark:text-gray-400">
          Filtri
        </h5>
        <button
          type="button"
          @click="isFiltersOpen = false"
          class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 inline-flex items-center dark:hover:bg-gray-600 dark:hover:text-white"
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 011.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            />
          </svg>
          <span class="sr-only">Chiudi</span>
        </button>
      </div>

      <MovieFiltersSidebar
        v-model:q="q"
        v-model:status="status"
        v-model:kind="kind"
        v-model:sortBy="sortBy"
        :stats="stats"
        @reset="resetFilters"
      />
    </div>
  </div>
</Transition>



    <!-- Empty state -->
    <div
      v-if="!loading && movies.length === 0"
      class="text-center opacity-80 py-12"
    >
      <div class="text-5xl mb-3">🍿</div>
      <div class="text-lg">Nessun film ancora. Aggiungine uno!</div>
    </div>

    <!-- Loader + sentinel -->
    <div ref="sentinel" class="h-10"></div>
    <!-- <div v-if="loading" class="text-sm opacity-70 py-4">Caricamento…</div> -->
    <div
      v-if="!hasMore && movies.length && !loading"
      class="text-center text-xs opacity-60 py-4"
    >
      Fine elenco
    </div>
  </div>

 <!-- Sidebar a destra (solo su desktop) -->
<div class="hidden lg:block">
  <MovieFiltersSidebar
    v-model:q="q"
    v-model:status="status"
    v-model:kind="kind"
    v-model:sortBy="sortBy"
    :stats="stats"
    @reset="resetFilters"
  />
</div>
</div>



  </div>
</template>

<style scoped>
.drawer-scroll {
  scrollbar-width: none;         /* Firefox */
}

/* Chrome, Edge, Safari */
.drawer-scroll::-webkit-scrollbar {
  display: none;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 300ms ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-12px);
}

.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}

.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}

.drawer-slide-enter-active,
.drawer-slide-leave-active {
  transition: transform 250ms ease, opacity 250ms ease;
}

.drawer-slide-enter-from,
.drawer-slide-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

.drawer-slide-enter-to,
.drawer-slide-leave-from {
  transform: translateX(0);
  opacity: 1;
}

</style>



<script setup>
import DashboardStats from '@/components/DashboardStats.vue'
import AddMovieForm from '@/components/AddMovieForm.vue'
import AddFromTmdb from '@/components/AddFromTmdb.vue'
import MovieCard from '@/components/MovieCard.vue'
import MovieCardSkeleton from '@/components/MovieCardSkeleton.vue'
import RandomPickerModal from '@/components/RandomPickerModal.vue'

import MovieFiltersSidebar from '@/components/MovieFiltersSidebar.vue'



definePageMeta({ layout: 'wide' })

const { user, isLoggedIn, init } = useAuth()   // 👈
onMounted(() => { init() })        

const showPicker = ref(false)
const showRandomPicker = ref(false)

// const prefillData = ref(null)
// function onPrefill(data) {
//   prefillData.value = data
//   showForm.value = true
// }

function onAddedFromTmdb(newMovie) {
  // prepend + ordina
  movies.value = sortClient([newMovie, ...movies.value], sortBy.value)
  fetchStats()
}

const { apiFetch } = useApi()

// --- Stats lato server
const stats = ref(null)
async function fetchStats() {
  try {
    stats.value = await apiFetch('/movies/stats')
  } catch (e) {
    console.error('stats error', e)
    stats.value = null
  }
}

const config = useRuntimeConfig()
const hasTmdb = computed(() => !!config.public.tmdbApiKey)

const movies = ref([])
const loading = ref(false)
const showForm = ref(false)

const q = ref('')
const status = ref('')
const sortBy = ref('created_at_desc')
const kind = ref('')
const isFiltersOpen = ref(false) // 👈 AGGIUNGI QUESTO

const limit = 20
let skip = 0
const hasMore = ref(true)
const sentinel = ref(null)
let observer

// Ordinamento client opzionale (manteniamo per aggiornamenti locali)
function sortClient(arr, key) {
  const a = [...arr]
  return a.sort((x, y) => {
    // 1) "In visione" prima
    const px = x.status === 'watching' ? 0 : 1
    const py = y.status === 'watching' ? 0 : 1
    if (px !== py) return px - py

    // 2) Ordinamento scelto
    if (key === 'title_asc') {
      return String(x.title || '').localeCompare(String(y.title || ''))
    }
    if (key === 'score_desc') {
      return (y.score || 0) - (x.score || 0)
    }
    // default: lascia l'ordine backend
    return 0
  })
}

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
    if (!status.value) params.set('priority_status', 'watching') // priorità "watching" in cima
    params.set('push_last_status', 'watched') // "watched" sempre in fondo

    const page = await apiFetch(`/movies/?${params.toString()}`)
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
  fetchStats()                 // carica subito le stats
  fetchMovies({ reset: true }) // e la prima pagina
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

// ---- Callbacks (uniche) ----
function onAdded(newMovie) {
  showForm.value = false
  // prepend e ri-ordina localmente se vuoi
  movies.value = sortClient([newMovie, ...movies.value], sortBy.value)
  fetchStats()
}

function onUpdated(updatedMovie) {
  const idx = movies.value.findIndex(m => m.id === updatedMovie.id)
  if (idx !== -1) {
    const next = [...movies.value]
    next[idx] = updatedMovie
    movies.value = sortClient(next, sortBy.value)
  }
  fetchStats()
}

function onDeleted(id) {
  movies.value = movies.value.filter(m => m.id !== id)
  fetchStats()
}
</script>
