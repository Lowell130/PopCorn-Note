<!-- pages/tv/[id].vue -->
<template>
  <div>
    <div class="mb-4 flex items-center gap-2 text-sm">
      <NuxtLink to="/" class="text-blue-300 hover:underline">← Torna alla dashboard</NuxtLink>
    </div>

    <div v-if="pending" class="opacity-70">Caricamento…</div>
    <div v-else-if="err" class="text-red-400">Errore: {{ err }}</div>
    <div v-else-if="!item" class="opacity-70">Elemento non trovato.</div>

    <div v-else class="bg-white text-black rounded-2xl p-5 shadow space-y-4">
      <h1 class="text-2xl font-semibold break-words">
        {{ item.title }}
        <span class="bg-yellow-100 text-yellow-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm dark:bg-yellow-900 dark:text-yellow-300">SERIE</span>
      </h1>

      <div class="flex flex-col md:flex-row gap-5">
        <img
          v-if="item.poster_url"
          :src="item.poster_url"
          alt=""
          class="w-40 h-60 rounded object-cover border self-start"
        />
        <div class="space-y-2 text-sm">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-2 mt-2">
            <div v-if="item.release_year"><span class="text-gray-500">Anno:</span> <span class="font-medium">{{ item.release_year }}</span></div>
            <div v-if="item.release_date"><span class="text-gray-500">Prima messa in onda:</span> <span class="font-medium">{{ item.release_date }}</span></div>
            <div v-if="item.runtime"><span class="text-gray-500">Durata ep.:</span> <span class="font-medium">{{ item.runtime }} min</span></div>
            <div v-if="item.director"><span class="text-gray-500">Creatore:</span> <span class="font-medium">{{ item.director }}</span></div>
            <div v-if="item.cast?.length" class="sm:col-span-2">
              <span class="text-gray-500">Cast:</span> <span class="font-medium">{{ item.cast.join(', ') }}</span>
            </div>
          </div>

          <div v-if="item.overview" class="pt-2">
            <div class="text-gray-500 mb-1">Trama</div>
            <p class="text-gray-800 whitespace-pre-line">{{ item.overview }}</p>
          </div>
        </div>
      </div>

      <!-- Selettori Stagione / Episodio -->
      <div v-if="item.tmdb_id" class="pt-3 border-t mt-2">
        <div class="grid sm:grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-medium mb-1">Stagione</label>
            <select v-model.number="selectedSeason" @change="loadEpisodes" class="w-full border rounded-lg p-2">
              <option v-for="s in seasons" :key="s.season_number" :value="s.season_number">
                {{ s.name || `Stagione ${s.season_number}` }} ({{ s.episode_count || 0 }} ep.)
              </option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Episodio</label>
            <select v-model.number="selectedEpisode" class="w-full border rounded-lg p-2">
              <option v-for="e in episodes" :key="e.episode_number" :value="e.episode_number">
                {{ e.episode_number }} — {{ e.name || 'Episodio' }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Player -->
    <ClientOnly>
      <div v-if="playerUrl" class="mt-6">
        <div class="text-sm opacity-70 mb-1">Player</div>
        <div class="rounded-xl overflow-hidden border border-white/10 bg-black/20">
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
</template>

<script setup>
const route = useRoute()
const { apiFetch } = useApi()

function isValidObjectId(id) {
  return typeof id === 'string' && /^[a-f0-9]{24}$/i.test(id)
}

definePageMeta({
  key: r => r.params.id
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

// appena ho l’item, carico stagioni
watch(item, async (it) => {
  if (!it?.tmdb_id) return
  const list = await apiFetch(`/tmdb/tv/${it.tmdb_id}/seasons`)
  seasons.value = list
  // default: prima stagione reale
  if (seasons.value.length) {
    selectedSeason.value = seasons.value[0].season_number
    await loadEpisodes()
  }
}, { immediate: true })

async function loadEpisodes() {
  if (!item.value?.tmdb_id || !selectedSeason.value) return
  episodes.value = await apiFetch(`/tmdb/tv/${item.value.tmdb_id}/season/${selectedSeason.value}`)
  if (episodes.value.length) {
    selectedEpisode.value = episodes.value[0].episode_number
  } else {
    selectedEpisode.value = 1
  }
}

const playerUrl = computed(() => {
  const id = item.value?.tmdb_id
  const s = selectedSeason.value
  const e = selectedEpisode.value
  return (id && s && e)
    ? `https://vixsrc.to/tv/${id}/${s}/${e}?lang=it&_=${Date.now()}`
    : null
})
</script>
