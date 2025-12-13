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
                <span class="text-gray-600">•</span> Creatore: <span class="text-white font-normal">{{ item.director }}</span>
              </span>
            </div>
            
            <!-- Progress Actions in Hero -->
            <div class="pt-2 flex flex-wrap items-center gap-3" v-if="item.last_watched">
               <button
                  type="button"
                  class="px-4 py-2 rounded-lg border border-white/30 bg-white/10 hover:bg-white/20 transition disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium backdrop-blur-sm"
                  :disabled="!item.last_watched"
                  @click="goToLastWatched()"
                  title="Vai all'ultimo episodio visto"
                >
                  Riprendi da S{{ item.last_watched.season }} E{{ item.last_watched.episode }}
                </button>
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
                        class="w-full appearance-none bg-black/50 border border-gray-700 text-white py-3 px-4 pr-8 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all cursor-pointer hover:bg-black/70"
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
                       <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 pt-6 text-gray-400">
                        <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                      </div>
                    </div>

                    <!-- Episode Selector -->
                     <div class="relative group">
                       <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Episodio</label>
                      <select
                        v-model.number="selectedEpisode"
                        class="w-full appearance-none bg-black/50 border border-gray-700 text-white py-3 px-4 pr-8 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all cursor-pointer hover:bg-black/70"
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
                      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 pt-6 text-gray-400">
                        <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                      </div>
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

               <!-- Player Frame -->
               <ClientOnly>
                <div v-if="playerUrl" class="rounded-2xl overflow-hidden shadow-2xl shadow-purple-900/20 border border-white/10 bg-black relative z-10 min-h-[300px]">
                  <div class="aspect-video w-full">
                     <iframe
                      :key="playerUrl"
                      :src="playerUrl"
                      class="w-full h-full"
                      allowfullscreen
                      allow="autoplay; fullscreen; encrypted-media"
                      referrerpolicy="no-referrer"
                    ></iframe>
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
                  <span 
                    v-for="actor in item.cast.slice(0, 8)" 
                    :key="actor" 
                    class="px-3 py-1 bg-black/40 hover:bg-black/60 transition rounded-full text-xs text-gray-200 border border-white/5"
                  >
                    {{ actor }}
                  </span>
                </div>
              </div>

              <div class="h-px bg-white/10 w-full"></div>

              <div class="space-y-4 text-sm">
                 <div v-if="item.director">
                  <span class="block text-gray-500 mb-1">Creatore</span>
                  <span class="text-white font-medium text-base">{{ item.director }}</span>
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
  </div>
</template>

<style scoped>
/* No custom css */
</style>

<script setup>
import RelatedTmdb from '@/components/RelatedTmdb.vue'

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
  return (id && s && e)
    ? `https://vixsrc.to/tv/${id}/${s}/${e}?lang=it&_=${Date.now()}`
    : null
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

onMounted(() => {
  refreshInterval = setInterval(() => {
    refreshToken()
  }, 9 * 60 * 1000) 
})

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval)
})
</script>
