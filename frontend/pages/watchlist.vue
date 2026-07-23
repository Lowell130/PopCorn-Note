<template>
  <div class="max-w-7xl mx-auto px-6 py-8 text-left">
    
    <!-- Title & Description -->
    <div class="border-b border-white/10 pb-6 mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
      <div>
        <h2 class="text-sm font-semibold text-purple-400 uppercase tracking-wider mb-1">
          La tua Collezione
        </h2>
        <h1 class="text-4xl font-extrabold text-white tracking-tight">
          La mia Watchlist
        </h1>
      </div>
      
      <!-- Guide Banner (Explain Watchlist) -->
      <p class="text-xs text-gray-400 max-w-md leading-relaxed">
        Salva i titoli che desideri guardare in futuro. Clicca sul segnalibro in Dashboard o esplora le novità.
      </p>
    </div>

    <!-- Info Box Banner -->
    <div class="bg-purple-950/10 border border-purple-500/20 p-5 rounded-3xl flex items-start gap-4 shadow-xl backdrop-blur-md mb-8">
      <div class="p-3 bg-purple-500/10 border border-purple-500/20 rounded-xl text-purple-300 flex-shrink-0 select-none">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
        </svg>
      </div>
      <div class="space-y-1 text-left">
        <h4 class="text-sm font-bold text-white">Come funziona la Watchlist?</h4>
        <p class="text-xs text-gray-400 leading-relaxed">
          Usa questa sezione per tenere traccia di film o serie che intendi iniziare. Passando alla scheda **Calendario Uscite**, 
          vedrai i countdown precisi e le date di debutto dei titoli non ancora usciti che hai aggiunto alla tua lista!
        </p>
      </div>
    </div>

    <!-- Tab navigation -->
    <div class="flex border-b border-white/10 mb-8 gap-4 select-none">
      <button
        @click="activeTab = 'list'"
        class="px-4 py-2.5 border-b-2 font-bold text-sm transition cursor-pointer"
        :class="activeTab === 'list' ? 'border-purple-500 text-purple-400' : 'border-transparent text-gray-400 hover:text-white'"
      >
        La mia Lista ({{ filteredWatchlist.length }})
      </button>
      <button
        @click="activeTab = 'calendar'"
        class="px-4 py-2.5 border-b-2 font-bold text-sm transition cursor-pointer"
        :class="activeTab === 'calendar' ? 'border-purple-500 text-purple-400' : 'border-transparent text-gray-400 hover:text-white'"
      >
        Calendario Uscite ({{ upcomingItems.length }})
      </button>
    </div>

    <!-- Spinner Loading -->
    <div v-if="loading" class="text-center py-20">
      <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-purple-500 mx-auto"></div>
    </div>

    <!-- Content Sections -->
    <div v-else>
      
      <!-- TAB 1: WATCHLIST LIST -->
      <div v-if="activeTab === 'list'">
        
        <!-- Filters & Search Bar -->
        <div class="flex flex-col sm:flex-row gap-3 mb-6 items-center">
          <input
            v-model="searchQuery"
            placeholder="Filtra per titolo..."
            class="w-full sm:flex-1 bg-white/5 border border-white/10 text-white placeholder-gray-500 rounded-xl px-4 py-2 text-xs focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all"
          />
          
          <div class="flex bg-white/5 border border-white/10 rounded-xl p-0.5" role="group">
            <button
              @click="filterType = 'all'"
              class="px-3.5 py-1 text-xs font-semibold rounded-lg transition cursor-pointer"
              :class="filterType === 'all' ? 'bg-purple-500/20 text-purple-300' : 'text-gray-400 hover:text-white'"
            >
              Tutti
            </button>
            <button
              @click="filterType = 'movie'"
              class="px-3.5 py-1 text-xs font-semibold rounded-lg transition cursor-pointer"
              :class="filterType === 'movie' ? 'bg-blue-500/20 text-blue-300' : 'text-gray-400 hover:text-white'"
            >
              Film
            </button>
            <button
              @click="filterType = 'tv'"
              class="px-3.5 py-1 text-xs font-semibold rounded-lg transition cursor-pointer"
              :class="filterType === 'tv' ? 'bg-yellow-500/20 text-yellow-300' : 'text-gray-400 hover:text-white'"
            >
              Serie TV
            </button>
          </div>
        </div>

        <!-- Empty state -->
        <div v-if="filteredWatchlist.length === 0" class="text-center py-20 text-gray-400">
          <svg class="w-16 h-16 mx-auto mb-4 opacity-20 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
          </svg>
          <p class="text-lg font-bold text-white">Nessun titolo trovato</p>
          <p class="mt-1 text-xs text-gray-500">Prova a cambiare i filtri o digita un nome diverso.</p>
        </div>

        <!-- Watchlist Grid -->
        <div v-else class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-5 gap-6">
          <div
            v-for="item in filteredWatchlist"
            :key="item.id"
            class="group relative bg-white/5 border border-white/10 rounded-2xl overflow-hidden shadow-lg transition hover:scale-105 hover:shadow-xl hover:z-10"
          >
            <!-- Poster Link -->
            <NuxtLink :to="item.type === 'movie' ? `/movies/${item.id}` : `/tv/${item.id}`" class="block aspect-[2/3] relative">
              <img
                v-if="item.poster"
                :src="`https://image.tmdb.org/t/p/w500${item.poster}`"
                :alt="item.title"
                class="w-full h-full object-cover transition duration-300 group-hover:opacity-75"
                loading="lazy"
              />
              <div v-else class="w-full h-full bg-white/5 flex items-center justify-center text-gray-500 text-xs">
                Nessun Poster
              </div>
              
              <!-- Overlay on Hover -->
              <div class="absolute inset-x-0 bottom-0 p-4 bg-gradient-to-t from-black/95 via-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end min-h-[50%]">
                 <h3 class="font-bold text-white text-xs line-clamp-2 leading-tight">{{ item.title }}</h3>
                 <p class="text-gray-400 text-[10px] mt-1">{{ item.release_year }} • {{ item.type === 'movie' ? 'Film' : 'Serie TV' }}</p>
              </div>
            </NuxtLink>

            <!-- Remove Button (Top Right) -->
            <button
              @click.prevent="removeItem(item.id)"
              class="absolute top-2 right-2 p-1.5 bg-black/60 hover:bg-red-600 text-white rounded-xl backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-all transform hover:scale-105 cursor-pointer shadow-md"
              title="Rimuovi dalla Watchlist"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

      </div>

      <!-- TAB 2: RELEASE CALENDAR TIMELINE -->
      <div v-if="activeTab === 'calendar'">
        
        <div v-if="upcomingItems.length === 0" class="text-center py-20 text-gray-400">
          <svg class="w-16 h-16 mx-auto mb-4 opacity-20 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          <p class="text-lg font-bold text-white">Nessuna uscita in programma</p>
          <p class="mt-1 text-xs text-gray-500">I titoli in arrivo nel tuo catalogo o con data futura appariranno qui.</p>
        </div>

        <div v-else class="space-y-4 max-w-3xl">
          <div
            v-for="item in upcomingItems"
            :key="item.id"
            class="flex items-center gap-4 bg-white/5 border border-white/10 p-4 rounded-3xl hover:bg-white/10 hover:border-white/20 transition-all duration-150 shadow-md backdrop-blur-md"
          >
            <!-- Poster icon -->
            <div class="w-12 h-18 bg-white/5 rounded-xl overflow-hidden flex-shrink-0 border border-white/5 shadow-sm">
              <img
                v-if="item.poster_url"
                :src="item.poster_url"
                class="w-full h-full object-cover"
                alt=""
                loading="lazy"
              />
              <div v-else class="w-full h-full flex items-center justify-center text-[10px] text-gray-500 font-bold">
                N/A
              </div>
            </div>

            <!-- Content details -->
            <div class="min-w-0 flex-1 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <div class="flex items-center gap-2">
                  <span
                    class="inline-flex items-center rounded-md text-[9px] font-bold px-2 py-0.5"
                    :class="item.kind === 'movie'
                      ? 'bg-blue-500/20 border border-blue-500/30 text-blue-300'
                      : 'bg-yellow-500/20 border border-yellow-500/30 text-yellow-300'"
                  >
                    {{ item.kind === 'movie' ? 'FILM' : 'SERIE' }}
                  </span>
                  
                  <NuxtLink :to="item.kind === 'tv' ? `/tv/${item.id}` : `/movies/${item.id}`" class="font-bold text-white hover:text-purple-400 transition-colors text-sm truncate">
                    {{ item.title }}
                  </NuxtLink>
                </div>
                
                <p class="text-xs text-gray-400 mt-1 font-medium flex items-center gap-1">
                  <svg class="w-3.5 h-3.5 text-purple-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                  Esce il: <span class="text-white">{{ formatDate(item.release_date) }}</span>
                </p>
              </div>

              <!-- Countdown display badge -->
              <span
                class="inline-flex items-center justify-center px-4 py-1.5 rounded-2xl text-xs font-black shadow-sm"
                :class="getCountdownClass(item.release_date)"
              >
                {{ getDaysRemaining(item.release_date) }}
              </span>
            </div>
          </div>
        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
definePageMeta({ middleware: 'auth' })

const { user, fetchMe } = useAuth()
const { apiFetch } = useApi()
const toast = useToast?.()

const loading = ref(true)
const activeTab = ref('list')
const searchQuery = ref('')
const filterType = ref('all')
const upcomingItems = ref([])

const watchlist = computed(() => {
    if (!user.value?.watchlist) return []
    return [...user.value.watchlist].sort((a, b) => new Date(b.added_at) - new Date(a.added_at))
})

const filteredWatchlist = computed(() => {
  let list = watchlist.value
  
  if (filterType.value !== 'all') {
    list = list.filter(item => item.type === filterType.value)
  }
  
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase().trim()
    list = list.filter(item => item.title.toLowerCase().includes(q))
  }
  
  return list
})

onMounted(async () => {
    if (user.value) {
        await Promise.all([
          fetchMe(),
          loadUpcoming()
        ])
    }
    loading.value = false
})

async function loadUpcoming() {
  try {
    const allMovies = await apiFetch('/movies/?upcoming_calendar=true&limit=500')
    const today = new Date().toISOString().split('T')[0]
    
    upcomingItems.value = allMovies
      .filter(m => (m.release_date && m.release_date >= today) || (!m.release_date && m.status === 'upcoming'))
      .sort((a, b) => {
        if (!a.release_date) return 1
        if (!b.release_date) return -1
        return new Date(a.release_date) - new Date(b.release_date)
      })
  } catch (e) {
    console.error(e)
  }
}

async function removeItem(id) {
    if (!confirm('Rimuovere questo elemento dalla watchlist?')) return

    try {
        await apiFetch(`/watchlist/${id}`, { method: 'DELETE' })
        if (user.value && user.value.watchlist) {
            user.value.watchlist = user.value.watchlist.filter(x => x.id !== id)
        }
        if (toast?.show) toast.show('success', 'Elemento rimosso dalla Watchlist')
    } catch (e) {
      console.error(e)
      if (toast?.show) toast.show('error', 'Errore durante la rimozione')
      await fetchMe()
    }
}

function formatDate(dateStr) {
  if (!dateStr) return 'N/A'
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateStr).toLocaleDateString('it-IT', options)
}

function getDaysRemaining(dateStr) {
  if (!dateStr) return 'N/D'
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  const targetDate = new Date(dateStr)
  targetDate.setHours(0, 0, 0, 0)
  
  const diffTime = targetDate - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) return 'Già disponibile'
  if (diffDays === 0) return 'Esce oggi!'
  if (diffDays === 1) return 'Domani!'
  return `Tra ${diffDays} giorni`
}

function getCountdownClass(dateStr) {
  if (!dateStr) return 'bg-white/5 border border-white/10 text-gray-400'
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  const targetDate = new Date(dateStr)
  targetDate.setHours(0, 0, 0, 0)
  
  const diffTime = targetDate - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) {
    return 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-400'
  }
  if (diffDays === 0 || diffDays === 1) {
    return 'bg-amber-500/20 border border-amber-500/35 text-amber-400 animate-pulse'
  }
  return 'bg-sky-500/10 border border-sky-500/20 text-sky-400'
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
