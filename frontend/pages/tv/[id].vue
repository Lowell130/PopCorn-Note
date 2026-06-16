<!-- pages/tv/[id].vue -->
<template>
  <div class="min-h-screen bg-black text-white font-sans selection:bg-purple-500 selection:text-white pb-20">
    <div v-if="pending" class="flex h-screen items-center justify-center">
      <div class="animate-pulse text-xl font-light tracking-widest text-gray-400">CARICAMENTO...</div>
    </div>
    <div v-else-if="err" class="flex h-screen items-center justify-center">
      <div class="text-red-400 text-lg">Errore: {{ err }}</div>
    </div>
    <div v-else-if="!item" class="flex h-screen items-center justify-center">
      <div class="text-gray-500">Elemento non trovato.</div>
    </div>

    <div v-else class="relative w-full">
      <!-- HERO SECTION -->
      <div class="relative w-full h-[70vh] lg:h-[85vh] overflow-hidden">
        <div 
          v-if="item.poster_url"
          class="absolute inset-0 bg-cover bg-center transition-transform duration-[10s] ease-out hover:scale-105"
          :style="{ backgroundImage: `url(${item.poster_url})` }"
        ></div>
        <div v-else class="absolute inset-0 bg-gray-900"></div>

        <div class="absolute inset-0 bg-gradient-to-t from-black via-black/60 to-transparent"></div>
        <div class="absolute inset-0 bg-gradient-to-r from-black via-black/40 to-transparent"></div>

        <!-- Hero Content -->
        <div class="absolute bottom-0 left-0 w-full p-6 md:p-12 lg:p-16 flex flex-col md:flex-row items-start md:items-end gap-8 max-w-7xl mx-auto z-10">
           <!-- Poster (Floating) -->
           <div class="hidden md:block w-48 lg:w-64 flex-shrink-0 shadow-2xl rounded-lg overflow-hidden border border-white/10 group">
            <img 
              v-if="item.poster_url" 
              :src="item.poster_url" 
              alt="Poster" 
              class="w-full h-auto object-cover transition-transform duration-500 group-hover:scale-110"
            />
          </div>

          <div class="flex-1 space-y-4 mb-4 md:mb-0 w-full">
             <div class="flex items-center gap-3 mb-2 flex-wrap">
              <span class="px-3 py-1 text-xs font-bold tracking-wider uppercase bg-purple-600/80 backdrop-blur-md rounded text-white shadow-lg shadow-purple-900/20">
                Serie TV
              </span>
              <!-- Badge Ultimo visto -->
              <span
                v-if="item?.last_watched"
                class="inline-flex items-center gap-1 px-3 py-1 text-xs font-medium bg-emerald-600/20 text-emerald-300 border border-emerald-500/30 backdrop-blur-md rounded"
                :title="lastWatchedTooltip"
              >
                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/></svg>
                Ultimo visto {{ lastWatchedLabel }}
              </span>
            </div>

            <h1 class="text-4xl md:text-5xl lg:text-7xl font-bold text-white leading-tight drop-shadow-lg text-left">
              {{ item.title }}
            </h1>

             <div class="flex flex-wrap items-center gap-x-2 md:gap-x-4 text-sm md:text-base text-gray-300 font-light">
              <span v-if="item.release_year">{{ item.release_year }}</span>
              <span v-if="item.release_year && item.runtime" class="text-gray-600">•</span>
              <span v-if="item.runtime">{{ item.runtime }} min/ep</span>
              <span v-if="item.director">
                <span class="text-gray-600">•</span> Creatore: <NuxtLink :to="{ path: '/dashboard', query: { director: item.director } }" class="text-blue-400 hover:text-blue-300 transition font-normal hover:underline">{{ item.director }}</NuxtLink>
              </span>
            </div>
            
            <!-- Progress Actions in Hero -->
            <div class="pt-2 flex flex-wrap items-center gap-3">
               <button
                  v-if="item.last_watched"
                  type="button"
                  class="px-4 py-2 rounded-lg border border-white/30 bg-white/10 hover:bg-white/20 transition disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium backdrop-blur-sm"
                  :disabled="!item.last_watched"
                  @click="goToLastWatched()"
                  title="Vai all'ultimo episodio visto"
                >
                  Riprendi da S{{ item.last_watched.season }} E{{ item.last_watched.episode }}
                </button>
                
                <button 
                  @click="showEditModal = true"
                  class="flex items-center gap-2 px-4 py-2 rounded-lg bg-green-600 hover:bg-green-700 text-white font-medium transition shadow-lg shadow-green-900/20"
                 >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                    Modifica
                 </button>
                 
               <WatchlistButton :item="item" type="tv" />
                <ShareButton :title="item.title" text="Sto guardando questa serie:" />
            </div>
          </div>
        </div>
      </div>

      <!-- MAIN CONTENT -->
      <div class="relative z-20 max-w-7xl mx-auto px-6 md:px-12 mt-8 md:mt-10 pb-12">
        
         <!-- Mobile Poster -->
        <div class="md:hidden mb-10 w-full max-w-sm mx-auto rounded-xl shadow-2xl overflow-hidden border border-white/20">
          <img 
              v-if="item.poster_url" 
              :src="item.poster_url" 
              alt="Poster" 
              class="w-full h-auto object-cover"
            />
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
          
          <!-- Left Column -->
          <div class="lg:col-span-2 space-y-10">

             <!-- Plot -->
             <div v-if="item.overview">
              <h3 class="text-xl font-semibold text-white mb-3 flex items-center gap-2">
                <span class="w-1 h-6 bg-purple-500 rounded-full"></span>
                Sinossi
              </h3>
              <p class="text-gray-300 leading-relaxed text-lg font-light whitespace-pre-line">
                {{ item.overview }}
              </p>
            </div>


            <!-- SELEZIONE EPISODI & PLAYER -->
            <div class="space-y-6" v-if="item.tmdb_id">
              <div class="flex items-center justify-between">
                <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                   <svg class="w-6 h-6 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                   Riproduzione
                </h3>
              </div>

              <!-- Selectors Container Glass -->
              <div class="p-6 bg-gray-900/60 backdrop-blur-xl border border-white/10 rounded-2xl space-y-4">
                  <div class="grid sm:grid-cols-2 gap-4">
                    <!-- Season Selector -->
                    <div class="relative group">
                      <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Stagione</label>
                      <select
                        v-model.number="selectedSeason"
                        @change="loadEpisodes"
                        class="w-full bg-black/50 border border-gray-700 text-white py-3 px-4 pr-8 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all cursor-pointer hover:bg-black/70"
                      >
                        <option
                          v-for="s in seasons"
                          :key="s.season_number"
                          :value="s.season_number"
                          class="bg-gray-900"
                        >
                          {{ s.name || `Stagione ${s.season_number}` }} ({{ s.episode_count || 0 }} ep.)
                        </option>
                      </select>
                    </div>

                    <!-- Episode Selector -->
                     <div class="relative group">
                       <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Episodio</label>
                      <select
                        v-model.number="selectedEpisode"
                        class="w-full bg-black/50 border border-gray-700 text-white py-3 px-4 pr-8 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all cursor-pointer hover:bg-black/70"
                      >
                         <option
                          v-for="e in episodes"
                          :key="e.episode_number"
                          :value="e.episode_number"
                          class="bg-gray-900"
                        >
                          {{ e.episode_number }} — {{ e.name || 'Episodio' }}
                        </option>
                      </select>
                    </div>
                  </div>

                  <!-- Action Row Inside Selector Box -->
                  <div class="flex items-center justify-end pt-2 border-t border-white/5 mt-2">
                     <button
                        type="button"
                        class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium transition shadow-lg shadow-emerald-900/50 disabled:opacity-50 disabled:cursor-not-allowed"
                        @click="markCurrentAsWatched()"
                        :disabled="savingProgress"
                        title="Segna come visto l'episodio selezionato"
                      >
                        <span v-if="!savingProgress">Segna episodio come visto</span>
                        <span v-else>Salvataggio...</span>
                         <svg v-if="!savingProgress" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                      </button>
                  </div>
              </div>





               <!-- Player Frame and Controls Wrapper -->
               <ClientOnly>
                <div 
                  v-if="playerUrl" 
                  ref="playerContainer" 
                  class="rounded-2xl overflow-hidden shadow-2xl shadow-purple-900/20 border border-white/10 bg-black relative z-10 min-h-[200px] md:min-h-[360px] group"
                  @mousemove="handleMouseMove"
                  @mouseleave="handleMouseLeave"
                >
                  <div class="aspect-video w-full relative z-0">
                     <iframe
                      ref="playerIframe"
                      :key="playerUrl"
                      :src="playerUrl"
                      class="w-full h-full"
                      allowfullscreen
                      allow="autoplay; fullscreen; encrypted-media"
                      referrerpolicy="no-referrer"
                    ></iframe>
                  </div>

                  <!-- Overlay Controls (Visible on mouse move) -->
                  <div 
                    class="absolute inset-0 z-20 flex items-end justify-center pb-8 transition-opacity duration-300 pointer-events-none bg-gradient-to-t from-black/60 via-transparent to-transparent"
                    :class="showControls ? 'opacity-100' : 'opacity-0'"
                  >
                     
                     <!-- Centered Control Pill -->
                     <div class="flex items-center gap-6 px-6 py-3 rounded-full bg-black/50 backdrop-blur-md border border-white/10 shadow-2xl pointer-events-auto transform transition hover:scale-105 hover:bg-black/70">
                        
                        <!-- Autoplay Toggle -->
                        <div class="flex items-center gap-3 border-r border-white/10 pr-6">
                           <label class="inline-flex items-center cursor-pointer">
                              <input type="checkbox" v-model="autoplayEnabled" class="sr-only peer">
                              <div class="relative w-9 h-5 bg-gray-600 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-purple-500 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-purple-600"></div>
                              <span class="ms-2 text-xs font-bold text-gray-200 uppercase tracking-wider">Autoplay</span>
                            </label>
                        </div>

                        <!-- Navigation & Fullscreen -->
                        <div class="flex items-center gap-3">
                           <button 
                             @click="prevEpisode"
                             :disabled="!canPrev"
                             class="p-2 rounded-full bg-white/5 hover:bg-white/20 disabled:opacity-30 disabled:cursor-not-allowed transition text-white"
                             title="Episodio precedente"
                           >
                              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/></svg> <!-- Material Design Skip Previous -->
                           </button>
       
                           <button 
                             @click="nextEpisode"
                             :disabled="!canNext"
                             class="p-2 rounded-full bg-white/5 hover:bg-white/20 disabled:opacity-30 disabled:cursor-not-allowed transition text-white"
                             title="Episodio successivo"
                           >
                              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/></svg> <!-- Material Design Skip Next -->
                           </button>
       
                           <!-- Fullscreen Toggle -->
                           <button 
                             @click="toggleFullscreen"
                             class="ml-2 p-2 rounded-full bg-white/5 hover:bg-white/20 transition text-white"
                             :title="isFullscreen ? 'Esci da schermo intero' : 'Schermo intero'"
                           >
                              <svg v-if="!isFullscreen" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"></path></svg>
                              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14H5.25m4.75 0v4.75m0-4.75l-4.75 4.75M14 10h4.75m-4.75 0V5.25m0 4.75l4.75-4.75"></path></svg>
                           </button>
                        </div>

                     </div>
                  </div>
                </div>
              </ClientOnly>
            </div>
            
          </div>

          <!-- Right Column Details -->
          <div class="space-y-8">
            <div class="p-6 rounded-2xl bg-white/5 backdrop-blur-md border border-white/10 space-y-6">
               <div v-if="item.cast?.length">
                <h4 class="text-sm font-bold text-gray-400 uppercase tracking-widest mb-3">Cast Principale</h4>
                <div class="flex flex-wrap gap-2">
                  <NuxtLink 
                    v-for="actor in item.cast.slice(0, 8)" 
                    :key="actor"
                    :to="{ path: '/dashboard', query: { cast: actor } }" 
                    class="px-3 py-1 bg-black/40 hover:bg-blue-900/40 transition rounded-full text-xs text-gray-200 border border-white/5 hover:border-blue-500/30 hover:text-blue-300"
                  >
                    {{ actor }}
                  </NuxtLink>
                </div>
              </div>

              <div class="h-px bg-white/10 w-full"></div>

              <div class="space-y-4 text-sm">
                 <div v-if="item.director">
                  <span class="block text-gray-500 mb-1">Creatore</span>
                  <NuxtLink :to="{ path: '/dashboard', query: { director: item.director } }" class="text-white hover:text-blue-300 hover:underline transition font-medium text-base">{{ item.director }}</NuxtLink>
                </div>
                <div v-if="item.release_date">
                  <span class="block text-gray-500 mb-1">Prima TV</span>
                  <span class="text-white font-medium">{{ item.release_date }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Related -->
        <div class="mt-20 pt-10 border-t border-white/10">
          <h3 class="text-2xl font-bold text-white mb-6">Potrebbe interessarti anche</h3>
           <RelatedTmdb
            v-if="tmdbIdNum"
            :kind="'tv'"
            :tmdb-id="tmdbIdNum"
          />
        </div>

      </div>
    </div>
    
    <EditReviewModal
      :show="showEditModal"
      :item="item"
      @close="showEditModal = false"
      @updated="handleUpdated"
      @deleted="handleDeleted"
    />
  </div>
</template>

<style scoped>
/* Gestione Fullscreen nativo */
:fullscreen {
  width: 100vw !important;
  height: 100vh !important;
  border-radius: 0 !important;
  border: none !important;
  background: black !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

:fullscreen .aspect-video {
  width: 100% !important;
  height: 100% !important;
  aspect-ratio: unset !important;
}

:fullscreen iframe {
  width: 100% !important;
  height: 100% !important;
}

/* Compatibilità WebKit (Safari/iOS) */
:-webkit-full-screen {
  width: 100vw !important;
  height: 100vh !important;
  border-radius: 0 !important;
  border: none !important;
  background: black !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

:-webkit-full-screen .aspect-video {
  width: 100% !important;
  height: 100% !important;
  aspect-ratio: unset !important;
}

:-webkit-full-screen iframe {
  width: 100% !important;
  height: 100% !important;
}
</style>

<script setup>
import RelatedTmdb from '@/components/RelatedTmdb.vue'
import EditReviewModal from '@/components/EditReviewModal.vue'

const showEditModal = ref(false)
const router = useRouter()

const route = useRoute()
const { apiFetch } = useApi()
const toast = useToast?.()
const savingProgress = ref(false)

function isValidObjectId(id) {
  return typeof id === 'string' && /^[a-f0-9]{24}$/i.test(id)
}

definePageMeta({
  layout: 'tv',
  key: r => r.params.id, 
})

const itemId = computed(() => String(route.params.id || ''))

const { data: item, pending, error } = await useAsyncData(
  () => `tv:${itemId.value}`,
  async () => {
    const id = itemId.value
    if (!isValidObjectId(id)) {
      throw createError({ statusCode: 400, statusMessage: 'ID non valido.' })
    }
    const it = await apiFetch(`/movies/${id}`)
    if (it.kind !== 'tv') {
      throw createError({ statusCode: 400, statusMessage: 'Questo elemento non è una serie TV.' })
    }
    return it
  },
  { watch: [itemId] }
)

const err = computed(() => error.value?.data?.message || error.value?.message || null)

// stagioni/episodi
const seasons = ref([])
const episodes = ref([])
const selectedSeason = ref(1)
const selectedEpisode = ref(1)

const lastWatchedLabel = computed(() => {
  const lw = item.value?.last_watched
  if (!lw) return ''
  const s = String(lw.season)
  const e = String(lw.episode).padStart(2, '0')
  return `S${s} • E${e}`
})

const lastWatchedTooltip = computed(() => {
  const lw = item.value?.last_watched
  if (!lw?.updated_at) return 'Ultimo episodio segnato come visto'
  const d = new Date(lw.updated_at)
  return `Segnato il ${d.toLocaleDateString()} ${d.toLocaleTimeString()}`
})

const initializedSeasons = ref(false)
const autoplayEnabled = ref(true)

// Navigation Computeds
const canNext = computed(() => {
  if (!episodes.value.length) return false
  // C'è un episodio dopo quello corrente?
  const curr = selectedEpisode.value
  const hasNextInSeason = episodes.value.some(e => e.episode_number === curr + 1)
  if (hasNextInSeason) return true
  
  // C'è una stagione successiva?
  const currSeas = selectedSeason.value
  const hasNextSeason = seasons.value.some(s => s.season_number === currSeas + 1)
  return hasNextSeason
})

const canPrev = computed(() => {
  if (!episodes.value.length) return false
  const curr = selectedEpisode.value
  // C'è un episodio prima?
  const hasPrevInSeason = episodes.value.some(e => e.episode_number === curr - 1)
  if (hasPrevInSeason) return true
  
  // C'è una stagione precedente?
  const currSeas = selectedSeason.value
  const hasPrevSeason = seasons.value.some(s => s.season_number === currSeas - 1)
  return hasPrevSeason
})

// Navigation Actions
async function nextEpisode() {
  if (!canNext.value) return
  
  const currentEpNum = selectedEpisode.value
  const nextEp = episodes.value.find(e => e.episode_number === currentEpNum + 1)
  
  if (nextEp) {
    selectedEpisode.value = nextEp.episode_number
  } else {
    // Next season
    selectedSeason.value = selectedSeason.value + 1
    // Il watcher gestirà il caricamento
  }
}

async function prevEpisode() {
  if (!canPrev.value) return

  const currentEpNum = selectedEpisode.value
  const prevEp = episodes.value.find(e => e.episode_number === currentEpNum - 1)
  
  if (prevEp) {
    selectedEpisode.value = prevEp.episode_number
  } else {
    // Prev season
    const prevSeasNum = selectedSeason.value - 1
    if (prevSeasNum < 1) return
    
    selectedSeason.value = prevSeasNum
  }
}

// carica stagioni/episodi la prima volta che abbiamo un tmdb_id
watch(
  () => item.value?.tmdb_id,
  async (tmdb) => {
    if (!tmdb) return
    const list = await apiFetch(`/tmdb/tv/${tmdb}/seasons`)
    seasons.value = list

    if (!initializedSeasons.value) {
      if (item.value?.last_watched) {
        selectedSeason.value = item.value.last_watched.season
        await loadEpisodes()
        const exists = episodes.value.find(
          e => e.episode_number === item.value.last_watched.episode
        )
        selectedEpisode.value = exists
          ? item.value.last_watched.episode
          : (episodes.value[0]?.episode_number ?? 1)
      } else {
        selectedSeason.value = seasons.value[0]?.season_number ?? 1
        await loadEpisodes()
        selectedEpisode.value = episodes.value[0]?.episode_number ?? 1
      }
      initializedSeasons.value = true
    }
  },
  { immediate: true }
)

// Watch per gestire i cambi di stagione (manualmente tramite select o programmaticamente per autoplay/navigazione)
watch(
  selectedSeason,
  async (newSeason, oldSeason) => {
    if (!newSeason) return
    await loadEpisodes()
    if (oldSeason !== undefined && oldSeason !== newSeason) {
      if (newSeason > oldSeason) {
        // Se avanziamo di stagione, iniziamo dal primo episodio
        selectedEpisode.value = episodes.value[0]?.episode_number ?? 1
      } else {
        // Se torniamo indietro di stagione, andiamo all'ultimo episodio
        selectedEpisode.value = episodes.value[episodes.value.length - 1]?.episode_number ?? 1
      }
    }
  }
)

async function loadEpisodes() {
  if (!item.value?.tmdb_id || !selectedSeason.value) return
  const prevEpisode = selectedEpisode.value
  episodes.value = await apiFetch(
    `/tmdb/tv/${item.value.tmdb_id}/season/${selectedSeason.value}`
  )
  const stillThere = episodes.value.find(e => e.episode_number === prevEpisode)
  selectedEpisode.value = stillThere
    ? prevEpisode
    : (episodes.value[0]?.episode_number ?? 1)
}

const playerUrl = computed(() => {
  const id = item.value?.tmdb_id
  const s = selectedSeason.value
  const e = selectedEpisode.value
  if (!id || !s || !e) return null
  let url = `https://vixsrc.to/tv/${id}/${s}/${e}?lang=it`
  if (autoplayEnabled.value) {
    url += '&autoplay=1'
  }
  return url
})

const tmdbIdNum = computed(() => {
  const x = item.value?.tmdb_id
  return typeof x === 'number' ? x : Number(x || 0)
})

function goToLastWatched() {
  const lw = item.value?.last_watched
  if (!lw) return
  selectedSeason.value = lw.season
  loadEpisodes().then(() => {
    const found = episodes.value.find(e => e.episode_number === lw.episode)
    selectedEpisode.value = found ? lw.episode : (episodes.value[0]?.episode_number ?? 1)
  })
}

async function markCurrentAsWatched() {
  if (!item.value?.id) return
  savingProgress.value = true
  try {
    const updated = await apiFetch(`/movies/${item.value.id}/progress`, {
      method: 'PUT',
      body: { season: selectedSeason.value, episode: selectedEpisode.value }
    })
    item.value = updated
    toast?.show?.('success', `Segnato S${selectedSeason.value} • E${selectedEpisode.value} come visto`)
  } catch (e) {
    console.error(e)
    toast?.show?.('error', 'Errore durante il salvataggio del progresso')
  } finally {
    savingProgress.value = false
  }
}



// Heartbeat sessione
const { refreshToken } = useAuth()
let refreshInterval = null

const showControls = ref(false)
let controlsTimeout = null

function handleMouseMove() {
  showControls.value = true
  if (controlsTimeout) clearTimeout(controlsTimeout)
  controlsTimeout = setTimeout(() => {
    showControls.value = false
  }, 3000)
}

function handleMouseLeave() {
  if (controlsTimeout) clearTimeout(controlsTimeout)
  showControls.value = false
}

const playerContainer = ref(null)
const isFullscreen = ref(false)

function toggleFullscreen() {
  if (!playerContainer.value) {
    toast?.show?.('error', 'Player non disponibile')
    return
  }

  const doc = document
  const el = playerContainer.value
  
  // Cross-browser fullscreen element check
  const fullscreenElement = doc.fullscreenElement || doc.webkitFullscreenElement || doc.mozFullScreenElement || doc.msFullscreenElement

  if (!fullscreenElement) {
    // Request Fullscreen (Cross-browser)
    const requestFs = el.requestFullscreen || el.webkitRequestFullscreen || el.mozRequestFullScreen || el.msRequestFullscreen
    
    if (requestFs) {
      requestFs.call(el).catch(err => {
        console.error(`Error attempting to enable fullscreen: ${err.message}`)
        toast?.show?.('error', `Errore Fullscreen: ${err.message}`)
      })
    } else {
      toast?.show?.('error', 'Fullscreen non supportato dal browser')
    }
  } else {
    // Exit Fullscreen (Cross-browser)
    const exitFs = doc.exitFullscreen || doc.webkitExitFullscreen || doc.mozCancelFullScreen || doc.msExitFullscreen
    
    if (exitFs) {
      exitFs.call(doc)
    }
  }
}

function onFullscreenChange() {
  const doc = document
  isFullscreen.value = !!(doc.fullscreenElement || doc.webkitFullscreenElement || doc.mozFullScreenElement || doc.msFullscreenElement)
}

/**
 * Gestione ciclo di vita
 */
onMounted(() => {
  refreshInterval = setInterval(() => {
    refreshToken()
  }, 9 * 60 * 1000)
  
  window.addEventListener('message', handlePlayerMessage)
  document.addEventListener('fullscreenchange', onFullscreenChange)
})

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval)
  window.removeEventListener('message', handlePlayerMessage)
  document.removeEventListener('fullscreenchange', onFullscreenChange)
})


function handlePlayerMessage(event) {
  let data = event.data
  
  // Log di debug in console per facilitare l'analisi dei messaggi del player
  console.log("PopCornNote - Messaggio ricevuto dal player:", data)

  // Gestione stringhe JSON o stringhe semplici
  if (typeof data === 'string') {
    try {
      data = JSON.parse(data)
    } catch (e) {
      // Se non è JSON, potrebbe essere una stringa diretta come "ended", "videoEnded" o "vidsrc_ended"
      if (data === 'ended' || data === 'videoEnded' || data === 'vidsrc_ended') {
        console.log("PopCornNote - Rilevata fine video (stringa):", data)
        handleEpisodeEnded()
        return
      }
    }
  }

  // Estrae l'evento da diversi possibili formati di oggetto
  const eventName = data?.event || data?.data?.event || data?.type

  if (
    eventName === 'ended' ||
    eventName === 'videoEnded' ||
    eventName === 'vidsrc_ended' ||
    (data?.type === 'PLAYER_EVENT' && data?.data?.event === 'ended')
  ) {
    console.log("PopCornNote - Rilevata fine video (oggetto):", data)
    handleEpisodeEnded()
  }
}


async function handleEpisodeEnded() {
  // 1. Segna come visto
  await markCurrentAsWatched()
  
  // Se l'autoplay è disabilitato, ci fermiamo qui (dopo aver salvato il progresso)
  if (!autoplayEnabled.value) return

  // 2. Calcola prossimo episodio
  const currentEpNum = selectedEpisode.value
  const currentSeasonNum = selectedSeason.value
  
  // Cerca nell'array episodi corrente se c'è un successivo
  // episodes.value è ordinato? Di solito sì da TMDB, ma cerchiamo per sicurezza
  // Assumiamo che episode_number sia sequenziale
  const nextInSeason = episodes.value.find(e => e.episode_number === currentEpNum + 1)
  
  if (nextInSeason) {
    // Caso semplice: prossimo episodio nella stessa stagione
    toast?.show?.('info', `Riproduzione episodio successivo: S${currentSeasonNum} E${nextInSeason.episode_number}`, 3000)
    selectedEpisode.value = nextInSeason.episode_number
  } else {
    // Caso fine stagione: cerchiamo la prossima stagione
    const nextSeasNum = currentSeasonNum + 1
    const nextSeasonExists = seasons.value.find(s => s.season_number === nextSeasNum)
    
    if (nextSeasonExists) {
      toast?.show?.('info', `Inizio prossima stagione: S${nextSeasNum}`, 3000)
      selectedSeason.value = nextSeasNum
    } else {
      toast?.show?.('success', 'Hai completato la serie!', 5000)
    }
  }
}


function handleUpdated(updatedItem) {
  item.value = updatedItem
}

function handleDeleted() {
  router.push('/dashboard')
}
</script>
