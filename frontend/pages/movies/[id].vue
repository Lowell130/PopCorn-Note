<!-- pages/movies/[id].vue -->
<template>
  <div class="min-h-screen bg-black text-white font-sans selection:bg-blue-500 selection:text-white pb-20">
    <div v-if="loading" class="flex h-screen items-center justify-center">
      <div class="animate-pulse text-xl font-light tracking-widest text-gray-400">CARICAMENTO...</div>
    </div>
    
    <div v-else-if="error" class="flex h-screen items-center justify-center">
      <div class="text-red-400 text-lg">Errore: {{ error }}</div>
    </div>
    
    <div v-else-if="!movie" class="flex h-screen items-center justify-center">
      <div class="text-gray-500">Film non trovato.</div>
    </div>

    <div v-else class="relative w-full">
      <!-- HERO SECTION -->
      <div class="relative w-full h-[70vh] lg:h-[85vh] overflow-hidden">
        <!-- Backdrop Image -->
        <div 
          v-if="movie.poster_url"
          class="absolute inset-0 bg-cover bg-center transition-transform duration-[10s] ease-out hover:scale-105"
          :style="{ backgroundImage: `url(${movie.poster_url})` }"
        ></div>
        <div v-else class="absolute inset-0 bg-gray-900"></div>

        <!-- Gradient Overlay -->
        <div class="absolute inset-0 bg-gradient-to-t from-black via-black/60 to-transparent"></div>
        <div class="absolute inset-0 bg-gradient-to-r from-black via-black/40 to-transparent"></div>

        <!-- Hero Content -->
        <div class="absolute bottom-0 left-0 w-full p-6 md:p-12 lg:p-16 flex flex-col md:flex-row items-start md:items-end gap-8 max-w-7xl mx-auto z-10">
          <!-- Poster (Floating) -->
          <div class="hidden md:block w-48 lg:w-64 flex-shrink-0 shadow-2xl rounded-lg overflow-hidden border border-white/10 group">
            <img 
              v-if="movie.poster_url" 
              :src="movie.poster_url" 
              alt="Poster" 
              class="w-full h-auto object-cover transition-transform duration-500 group-hover:scale-110"
            />
          </div>

          <!-- Title & Meta -->
          <div class="flex-1 space-y-4 mb-4 md:mb-0 w-full">
            <div class="flex items-center gap-3 mb-2">
              <span class="px-3 py-1 text-xs font-bold tracking-wider uppercase bg-blue-600/80 backdrop-blur-md rounded text-white shadow-lg shadow-blue-900/20">
                Movie
              </span>
              <span v-if="movie.score" class="flex items-center gap-1 text-orange-400 font-medium">
                <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                {{ movie.score }}/10
              </span>
            </div>
            
            <h1 class="text-4xl md:text-5xl lg:text-7xl font-bold text-white leading-tight drop-shadow-lg text-left">
              {{ movie.title }}
            </h1>
            
            <div class="flex flex-wrap items-center gap-x-2 md:gap-x-4 text-sm md:text-base text-gray-300 font-light">
              <span v-if="movie.release_year">{{ movie.release_year }}</span>
              <span v-if="movie.release_year && movie.runtime" class="text-gray-600">•</span>
              <span v-if="movie.runtime">{{ movie.runtime }} min</span>
              <span v-if="movie.director">
                <span class="text-gray-600">•</span> Regia di <span class="text-white font-normal">{{ movie.director }}</span>
              </span>
            </div>

            <!-- Action Buttons Row (Optional future actions) -->
             <div class="pt-4 flex gap-3" v-if="false">
                 <!-- Placeholder per pulsanti "Play", "Aggiungi a lista", ecc. -->
             </div>
          </div>
        </div>
      </div>
      
      <!-- DETAILS & CONTENT SECTION -->
      <div class="relative z-20 max-w-7xl mx-auto px-6 md:px-12 mt-8 md:mt-10 pb-12">
        
        <!-- Mobile Poster (Visible only on small screens) -->
        <div class="md:hidden mb-10 w-full max-w-sm mx-auto rounded-xl shadow-2xl overflow-hidden border border-white/20">
          <img 
              v-if="movie.poster_url" 
              :src="movie.poster_url" 
              alt="Poster" 
              class="w-full h-auto object-cover"
            />
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
          
          <!-- Left Column: Storyline & Player -->
          <div class="lg:col-span-2 space-y-10">
            
            <!-- Plot -->
            <div v-if="movie.overview">
              <h3 class="text-xl font-semibold text-white mb-3 flex items-center gap-2">
                <span class="w-1 h-6 bg-blue-500 rounded-full"></span>
                Trama
              </h3>
              <p class="text-gray-300 leading-relaxed text-lg font-light whitespace-pre-line">
                {{ movie.overview }}
              </p>
            </div>

            <!-- Note (se presente) -->
            <div v-if="movie.note" class="bg-gray-800/50 border border-gray-700 p-4 rounded-xl">
              <h4 class="text-sm font-bold text-gray-400 uppercase tracking-widest mb-1">Nota Personale</h4>
              <p class="text-gray-200 italic">{{ movie.note }}</p>
            </div>
            
            <!-- Player Section -->
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                   <svg class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                   Riproduzione
                </h3>
              </div>
              
              <ClientOnly>
                <div v-if="playerUrl" class="rounded-2xl overflow-hidden shadow-2xl shadow-blue-500/10 border border-white/10 bg-black relative z-10">
                  <div class="aspect-video w-full">
                     <iframe
                      :src="playerUrl"
                      class="w-full h-full"
                      allowfullscreen
                      referrerpolicy="no-referrer"
                    ></iframe>
                  </div>
                </div>
                <div v-else class="h-64 flex items-center justify-center bg-gray-900 rounded-2xl border border-gray-800 text-gray-500">
                  Player non disponibile (ID mancante)
                </div>
              </ClientOnly>
            </div>

          </div>

          <!-- Right Column: Details Sidebar -->
          <div class="space-y-8">
            <!-- Glassmorphism Card -->
            <div class="p-6 rounded-2xl bg-white/5 backdrop-blur-md border border-white/10 space-y-6">
              
              <!-- Cast -->
              <div v-if="movie.cast?.length">
                <h4 class="text-sm font-bold text-gray-400 uppercase tracking-widest mb-3">Cast Principale</h4>
                <div class="flex flex-wrap gap-2">
                  <span 
                    v-for="actor in movie.cast.slice(0, 10)" 
                    :key="actor" 
                    class="px-3 py-1 bg-black/40 hover:bg-black/60 transition rounded-full text-xs text-gray-200 border border-white/5"
                  >
                    {{ actor }}
                  </span>
                </div>
              </div>

              <div class="h-px bg-white/10 w-full"></div>

              <!-- Information Grid -->
              <div class="space-y-4 text-sm">
                 <div v-if="movie.director">
                  <span class="block text-gray-500 mb-1">Regia</span>
                  <span class="text-white font-medium text-base">{{ movie.director }}</span>
                </div>
                <div v-if="movie.release_date">
                  <span class="block text-gray-500 mb-1">Data Uscita</span>
                  <span class="text-white font-medium">{{ movie.release_date }}</span>
                </div>
                 <div v-if="movie.liked">
                  <span class="block text-gray-500 mb-1">Il tuo voto</span>
                   <span class="inline-block px-2 py-1 rounded bg-white/10 border border-white/10 text-white font-medium">
                    {{ likedLabel(movie.liked) }}
                  </span>
                </div>
              </div>

            </div>

             <!-- Related Section Placeholder Position -->
             <!-- Potrebbe andare qui o sotto tutto il contenuto principale -->
          </div>
        </div>

        <!-- Correlati (Full Width) -->
        <div class="mt-20 pt-10 border-t border-white/10">
          <h3 class="text-2xl font-bold text-white mb-6">Potrebbe interessarti anche</h3>
          <RelatedTmdb
            v-if="tmdbIdNum"
            :kind="'movie'"
            :tmdb-id="tmdbIdNum"
          />
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
/* Nessuno stile custom CSS necessario, tutto gestito via Tailwind */
</style>

<script setup>
import StatusBadge from '@/components/StatusBadge.vue'
import RelatedTmdb from '@/components/RelatedTmdb.vue'

const route = useRoute()
const { apiFetch } = useApi()
const toast = useToast()

// helper: ObjectId valido (24 hex)
function isValidObjectId(id) {
  return typeof id === 'string' && /^[a-f0-9]{24}$/i.test(id)
}

// Forza remount della pagina per ogni id
definePageMeta({
  layout: 'movies',
  key: r => r.params.id, 
})

const movieId = computed(() => String(route.params.id || ''))

const { data: movie, pending: loading, error } = await useAsyncData(
  () => `movie:${movieId.value}`,
  async () => {
    const id = movieId.value
    if (!isValidObjectId(id)) {
      throw createError({ statusCode: 400, statusMessage: 'ID film non valido.' })
    }
    return await apiFetch(`/movies/${id}`)
  },
  {
    watch: [movieId],
  }
)

const likedOptions = [
  { value: 'loved', label: 'Mi è piaciuto molto' },
  { value: 'liked', label: 'Mi è piaciuto' },
  { value: 'okay', label: 'Carino' },
  { value: 'disliked', label: 'Non mi è piaciuto' },
  { value: 'terrible', label: 'Pessimo' }
]
function likedLabel(val) {
  return likedOptions.find(l => l.value === val)?.label || val
}

// Azione TMDb (logica esistente mantenuta, anche se UI nascosta/rimossa per pulizia nel nuovo design, 
// o reintrodurla se l'utente la richiede esplicitamente. Nel template sopra l'ho omessa per focus visuale, 
// ma la funzione resta disponibile nel setup se volessimo collegarla a un pulsante edit)
const loadingAction = ref(false)
async function completeFromTmdb() {
  if (!movie.value) return
  loadingAction.value = true
  try {
    let tmdbId = movie.value.tmdb_id
    if (!tmdbId) {
      const q = window.prompt('Cerca su TMDb:', movie.value.title || '')
      if (!q || !q.trim()) { loadingAction.value = false; return }
      const results = await apiFetch('/tmdb/search', { query: { q: q.trim() } })
      if (!Array.isArray(results) || results.length === 0) {
        toast.show('error', 'Nessun risultato trovato su TMDb.')
        loadingAction.value = false
        return
      }
      const top = results[0]
      if (!window.confirm(`Usare "${top.title}" (${top.release_date || '—'})?`)) {
        loadingAction.value = false
        return
      }
      tmdbId = top.id
    }

    const details = await apiFetch(`/tmdb/details/${tmdbId}`)
    const payload = {
      tmdb_id: details.tmdb_id ?? tmdbId,
      release_date: details.release_date || undefined,
      release_year: details.release_year ?? undefined,
      poster_url: details.poster_url || undefined,
      director: details.director || undefined,
      cast: Array.isArray(details.cast) ? details.cast : undefined,
      runtime: details.runtime ?? undefined
    }
    const updated = await apiFetch(`/movies/${movieId.value}`, { method: 'PUT', body: payload })
    movie.value = updated
    toast.show('success', 'Dati completati da TMDb.')
  } catch (e) {
    console.error(e)
    toast.show('error', 'Errore durante il completamento da TMDb.')
  } finally {
    loadingAction.value = false
  }
}

const playerUrl = computed(() => {
  const id = movie.value?.tmdb_id
  return id ? `https://vixsrc.to/movie/${id}?lang=it` : null
})

const tmdbIdNum = computed(() => {
  const x = movie.value?.tmdb_id
  return typeof x === 'number' ? x : Number(x || 0)
})

const { refreshToken } = useAuth()
let refreshInterval = null

onMounted(() => {
  refreshInterval = setInterval(() => {
    refreshToken()
  }, 9 * 60 * 1000) 
})

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval)
})
</script>

