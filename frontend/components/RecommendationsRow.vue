<template>
  <div v-if="recommendations.length" class="mb-8 animate-fade-in">
    <div class="flex items-center gap-2 mb-3 px-1">
      <h3 class="text-lg font-semibold text-gray-800 dark:text-white">
        ✨ Perché hai aggiunto <span class="bg-gradient-to-r from-purple-500 to-pink-500 bg-clip-text text-transparent">{{ sourceMovie?.title }}</span>
      </h3>
    </div>

    <div class="relative group">
      <!-- Scroll Buttons -->
      <button 
        v-if="canScrollLeft"
        @click="scroll('left')"
        class="absolute left-0 top-1/2 -translate-y-1/2 z-10 w-8 h-8 flex items-center justify-center bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-full shadow-lg text-gray-800 dark:text-white hover:scale-110 transition opacity-0 group-hover:opacity-100 disabled:opacity-0"
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>

      <button 
        v-if="canScrollRight"
        @click="scroll('right')"
        class="absolute right-0 top-1/2 -translate-y-1/2 z-10 w-8 h-8 flex items-center justify-center bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-full shadow-lg text-gray-800 dark:text-white hover:scale-110 transition opacity-0 group-hover:opacity-100 disabled:opacity-0"
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>

      <!-- Scroll Container -->
      <div 
        ref="scrollContainer"
        class="flex gap-4 overflow-x-auto pb-4 px-1 snap-x snap-mandatory scrollbar-hide scroll-smooth"
        style="scrollbar-width: none; -ms-overflow-style: none;"
        @scroll="checkScroll"
      >
        <div 
          v-for="rec in recommendations" 
          :key="rec.id"
          class="flex-shrink-0 w-36 snap-start group/card relative"
        >
          <!-- Card -->
          <div class="relative aspect-[2/3] rounded-xl overflow-hidden shadow-md transition-transform hover:scale-105 bg-gray-200">
            <img 
              v-if="rec.poster_url" 
              :src="rec.poster_url" 
              class="w-full h-full object-cover" 
              loading="lazy" 
            />
            <div v-else class="w-full h-full flex items-center justify-center text-xs text-gray-400">
              No Poster
            </div>

            <!-- Overlay Actions -->
            <div class="absolute inset-0 bg-black/60 opacity-0 group-hover/card:opacity-100 transition-opacity flex flex-col items-center justify-center gap-2 p-2">
              <button 
                @click="addRecommendation(rec)"
                class="w-full py-1.5 bg-emerald-500 hover:bg-emerald-600 text-white text-xs font-bold rounded-full shadow-lg transform transition-transform active:scale-95 flex items-center justify-center gap-1"
                :disabled="addingId === rec.id"
              >
                <span v-if="addingId === rec.id" class="animate-spin">⌛</span>
                <span v-else>+ Aggiungi</span>
              </button>
              
              <a 
                :href="`https://www.themoviedb.org/${rec.kind === 'tv' ? 'tv' : 'movie'}/${rec.tmdb_id}`"
                target="_blank"
                class="w-full py-1.5 bg-white/20 hover:bg-white/30 text-white text-xs font-medium rounded-full text-center backdrop-blur-sm"
              >
                Info
              </a>
            </div>
          </div>

          <!-- Title -->
          <div class="mt-2">
            <h4 class="text-xs font-medium text-gray-900 dark:text-gray-100 truncate" :title="rec.title">
              {{ rec.title }}
            </h4>
            <div class="flex items-center justify-between text-[10px] text-gray-500">
              <span>{{ rec.release_year || 'N/A' }}</span>
              <span v-if="rec.vote_average" class="flex items-center gap-0.5 text-amber-500">
                ★ {{ rec.vote_average.toFixed(1) }}
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Gradient Fade Edges (optional polish) -->
      <div class="absolute inset-y-0 right-0 w-12 bg-gradient-to-l from-white dark:from-gray-900 to-transparent pointer-events-none lg:hidden"></div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  sourceMovie: { type: Object, default: null }
})

const emit = defineEmits(['added'])
const { apiFetch } = useApi()
const toast = useToast?.()

const recommendations = ref([])
const loading = ref(false)
const addingId = ref(null)
const scrollContainer = ref(null)

const canScrollLeft = ref(false)
const canScrollRight = ref(true)

function checkScroll() {
  const el = scrollContainer.value
  if (!el) return
  canScrollLeft.value = el.scrollLeft > 0
  canScrollRight.value = el.scrollLeft + el.clientWidth < el.scrollWidth - 10
}

function scroll(direction) {
  const el = scrollContainer.value
  if (!el) return
  const scrollAmount = el.clientWidth * 0.8
  el.scrollBy({
    left: direction === 'left' ? -scrollAmount : scrollAmount,
    behavior: 'smooth'
  })
}

// Watch sourceMovie changes to fetch new recommendations
watch(() => props.sourceMovie, async (newVal) => {
  if (!newVal || !newVal.tmdb_id) return
  await fetchRecommendations(newVal)
  // Check scroll initially after render
  setTimeout(checkScroll, 100)
}, { immediate: true })

async function fetchRecommendations(movie) {
  loading.value = true
  recommendations.value = []
  try {
    const kind = movie.kind === 'tv' ? 'tv' : 'movie'
    // Endpoint: /tmdb/{kind}/{id}/recommendations
    const res = await apiFetch(`/tmdb/${kind}/${movie.tmdb_id}/recommendations`)
    // Filter out items without posters to keep it pretty, take top 10
    recommendations.value = (res.results || [])
      .filter(r => r.poster_url)
      .slice(0, 10)
  } catch (e) {
    console.error('Recs fetch error', e)
  } finally {
    loading.value = false
  }
}

async function addRecommendation(rec) {
  addingId.value = rec.id
  try {
    // Reuse logic: fetch full details then save
    // We assume backend endpoints exist as checked: /tmdb/details/{id} or /tmdb/tv/{id}
    const kind = rec.kind
    let details
    if (kind === 'tv') {
      details = await apiFetch(`/tmdb/tv/${rec.id}`) // endpoint returns 'tmdb_id' in response usually
    } else {
      details = await apiFetch(`/tmdb/details/${rec.id}`)
    }

    const payload = {
      kind: kind,
      title: details.title,
      status: 'to_watch',
      release_date: details.release_date || null,
      release_year: details.release_year ?? null,
      poster_url: details.poster_url || null,
      director: details.director || null,
      cast: Array.isArray(details.cast) ? details.cast : null,
      runtime: details.runtime ?? null,
      tmdb_id: details.tmdb_id || rec.id,
      overview: details.overview || null,
      tmdb_vote: details.vote_average ?? null
    }

    const saved = await apiFetch('/movies/', {
      method: 'POST',
      body: payload
    })

    toast?.show?.('success', `"${saved.title}" aggiunto!`)
    emit('added', saved)
    
    // Remove from list to avoid duplicate adding visually
    recommendations.value = recommendations.value.filter(r => r.id !== rec.id)
    
  } catch (e) {
    console.error('Add rec error', e)
    if (e.response?.status === 409) {
      toast?.show?.('error', 'Già presente nella lista!')
    } else {
      toast?.show?.('error', 'Errore durante l\'aggiunta')
    }
  } finally {
    addingId.value = null
  }
}
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
