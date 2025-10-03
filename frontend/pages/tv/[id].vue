<!-- pages/tv/[id].vue -->
<template>
  <div>
    <!-- <div class="mb-4 flex items-center gap-2 text-sm">
      <NuxtLink to="/" class="text-blue-300 hover:underline">← Torna alla dashboard</NuxtLink>
    </div> -->

    <div v-if="pending" class="opacity-70">Caricamento…</div>
    <div v-else-if="err" class="text-red-400">Errore: {{ err }}</div>
    <div v-else-if="!item" class="opacity-70">Elemento non trovato.</div>

  <!-- <div
  v-else
  class="relative rounded-2xl overflow-hidden shadow"
> -->
  <div
  v-else
  class="relative overflow-hidden shadow"
>
  <!-- Poster come sfondo -->
  <div
    v-if="item.poster_url"
    class="absolute inset-0 bg-center bg-cover"
    :style="{ backgroundImage: `url(${item.poster_url})` }"
  ></div>

  <!-- Overlay scuro per leggibilità -->
  <div class="absolute inset-0 bg-black/90"></div>

  <!-- Contenuto sopra -->
  <div class="relative z-10 my-7 p-5 space-y-4 text-white max-w-7xl mx-auto">
   <h1 class="text-2xl font-semibold break-words">
  {{ item.title }}
  <span
    class="bg-yellow-100 text-yellow-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm"
  >
    SERIE
  </span>

  <!-- ✅ Badge Ultimo visto -->
  <span
    v-if="item?.last_watched"
    class="inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium bg-emerald-600/90 text-white align-middle"
    :title="lastWatchedTooltip"
  >
    <!-- piccola iconcina -->
    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/>
    </svg>
    Ultimo visto {{ lastWatchedLabel }}
  </span>
</h1>


<!-- Dentro il blocco principale, sotto il titolo/infos, PRIMA dei selettori -->
<!-- Barra progresso sempre visibile -->
<div class="mt-2 flex flex-wrap items-center gap-2 text-sm">
  <span class="inline-flex items-center gap-2 rounded-lg bg-black/40 px-3 py-1">
    <template v-if="item.last_watched">
      Ultimo visto:
      <strong>S{{ item.last_watched.season }} • E{{ item.last_watched.episode }}</strong>
    </template>
    <template v-else>
      Nessun episodio segnato
    </template>
  </span>

  <button
    type="button"
    class="px-3 py-1.5 rounded border border-white/30 bg-white/10 hover:bg-white/20 transition disabled:opacity-50 disabled:cursor-not-allowed"
    :disabled="!item.last_watched"
    @click="goToLastWatched()"
    title="Vai all'ultimo episodio visto"
  >
    Vai
  </button>

  <button
    type="button"
    class="px-3 py-1.5 rounded bg-emerald-600 hover:bg-emerald-700 transition text-white disabled:opacity-50 disabled:cursor-not-allowed"
    @click="markCurrentAsWatched()"
    :disabled="savingProgress"
    title="Segna come visto l'episodio selezionato"
  >
    <span v-if="!savingProgress">Segna come visto</span>
    <span v-else>Salvo…</span>
  </button>
</div>

  <div class="flex flex-col md:flex-row gap-5">
  <!-- Poster piccolo -->
  <img
    v-if="item.poster_url"
    :src="item.poster_url"
    alt=""
    class="w-full md:w-40 h-auto md:h-60 rounded object-cover border self-start md:flex-shrink-0"
  />

      <!-- Info -->
      <div class="space-y-2 text-sm">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-2 mt-2">
          <div v-if="item.release_year">
            <span class="text-gray-300">Anno:</span>
            <span class="font-medium">{{ item.release_year }}</span>
          </div>
          <div v-if="item.release_date">
            <span class="text-gray-300">Prima messa in onda:</span>
            <span class="font-medium">{{ item.release_date }}</span>
          </div>
          <div v-if="item.runtime">
            <span class="text-gray-300">Durata ep.:</span>
            <span class="font-medium">{{ item.runtime }} min</span>
          </div>
          <div v-if="item.director">
            <span class="text-gray-300">Creatore:</span>
            <span class="font-medium">{{ item.director }}</span>
          </div>
          <div v-if="item.cast?.length" class="sm:col-span-2">
            <span class="text-gray-300">Cast:</span>
            <span class="font-medium">{{ item.cast.join(', ') }}</span>
          </div>
        </div>

        <div v-if="item.overview" class="pt-2">
          <div class="text-gray-300 mb-1">Trama</div>
          <p class="whitespace-pre-line">{{ item.overview }}</p>
        </div>
      </div>
    </div>

    <!-- Selettori Stagione / Episodio -->
    <div v-if="item.tmdb_id" class="pt-3 border-t border-white/20 mt-2">
      <div class="grid sm:grid-cols-2 gap-3">
        <div>
          <label class="block text-xs font-medium mb-1 text-gray-300">Stagione</label>
          <select
            v-model.number="selectedSeason"
            @change="loadEpisodes"
            class="w-full border rounded-lg p-2 bg-black/40 border-gray-600 text-white"
          >
            <option
              v-for="s in seasons"
              :key="s.season_number"
              :value="s.season_number"
            >
              {{ s.name || `Stagione ${s.season_number}` }} ({{ s.episode_count || 0 }} ep.)
            </option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-medium mb-1 text-gray-300">Episodio</label>
          <select
            v-model.number="selectedEpisode"
            class="w-full border rounded-lg p-2 bg-black/40 border-gray-600 text-white"
          >
            <option
              v-for="e in episodes"
              :key="e.episode_number"
              :value="e.episode_number"
            >
              {{ e.episode_number }} — {{ e.name || 'Episodio' }}
            </option>
          </select>
        </div>
      </div>
    </div>
  </div>
</div>

    <!-- Player -->
    <div class="bg-player">
    <div class="max-w-7xl mx-auto px-4 py-6">
    <ClientOnly>
      <div v-if="playerUrl" class="mt-6">
        <!-- <h3 class="text-lg font-semibold text-black mb-4">Player</h3> -->
        <div class="overflow-hidden border border-white/10 bg-black/20">
          <iframe
          :key="playerUrl"  
            :src="playerUrl"
            class="w-full"
            style="aspect-ratio: 16 / 9"
            frameborder="0"
            allowfullscreen
            referrerpolicy="no-referrer"
          ></iframe>
        </div>
      </div>
    </ClientOnly>
</div>
</div>
      <!-- Correlati -->
      <div class="max-w-7xl mx-auto px-4 py-6">
  <RelatedTmdb
    v-if="tmdbIdNum"
    :kind="'tv'"
    :tmdb-id="tmdbIdNum"
  />
  </div>
  </div>
</template>

<style scoped>
.bg-player {
	background: linear-gradient(-45deg, #000000, #3a3a3a, #000000, #262626);
	background-size: 400% 400%;
	animation: gradient 15s ease infinite;
	
}

@keyframes gradient {
	0% {
		background-position: 0% 50%;
	}
	50% {
		background-position: 100% 50%;
	}
	100% {
		background-position: 0% 50%;
	}
}

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
  key: r => r.params.id, // forza remount quando cambia l'id
})

const itemId = computed(() => String(route.params.id || ''))

// carico l’item (deve essere kind=tv)
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
// const pending = pending

// stagioni/episodi
const seasons = ref([])
const episodes = ref([])
const selectedSeason = ref(1)
const selectedEpisode = ref(1)

const lastWatchedLabel = computed(() => {
  const lw = item.value?.last_watched
  if (!lw) return ''
  // zero-pad opzionale sugli episodi (tipo E03)
  const s = String(lw.season)
  const e = String(lw.episode).padStart(2, '0')
  return `S${s} • E${e}`
})

const lastWatchedTooltip = computed(() => {
  const lw = item.value?.last_watched
  if (!lw?.updated_at) return 'Ultimo episodio segnato come visto'
  const d = new Date(lw.updated_at)
  // fallback semplice e locale-friendly
  return `Segnato il ${d.toLocaleDateString()} ${d.toLocaleTimeString()}`
})

// Sostituisci il vecchio watch(...) con questo:

const initializedSeasons = ref(false)

// carica stagioni/episodi la prima volta che abbiamo un tmdb_id
watch(
  () => item.value?.tmdb_id,
  async (tmdb) => {
    if (!tmdb) return
    const list = await apiFetch(`/tmdb/tv/${tmdb}/seasons`)
    seasons.value = list

    // inizializza SOLO la prima volta
    if (!initializedSeasons.value) {
      if (item.value?.last_watched) {
        // parti dall'ultimo visto
        selectedSeason.value = item.value.last_watched.season
        await loadEpisodes()
        const exists = episodes.value.find(
          e => e.episode_number === item.value.last_watched.episode
        )
        selectedEpisode.value = exists
          ? item.value.last_watched.episode
          : (episodes.value[0]?.episode_number ?? 1)
      } else {
        // altrimenti prima stagione/episodio disponibili
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
  // se l'episodio precedente esiste ancora, mantienilo
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
  // ricarica gli episodi di quella stagione e poi setta episodio
  loadEpisodes().then(() => {
    // se esiste quell'episodio, selezionalo, altrimenti fallback 1
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
    // aggiorna localmente l'item
    item.value = updated
    toast?.show?.('success', `Segnato S${selectedSeason.value} • E${selectedEpisode.value} come visto`)
  } catch (e) {
    console.error(e)
    toast?.show?.('error', 'Errore durante il salvataggio del progresso')
  } finally {
    savingProgress.value = false
  }
}

</script>
