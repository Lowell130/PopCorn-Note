<template>
  <div class="bg-white text-black rounded-2xl p-5 shadow space-y-3">
    <div class="flex items-center justify-between gap-3">
      <h2 class="text-lg font-semibold">
        In uscita (prossimi {{ months }} mesi)
      </h2>

      <div class="flex items-center gap-2 text-sm">
        <label class="opacity-70">Pagina</label>
        <select v-model.number="page" class="border rounded px-2 py-1">
          <option v-for="p in totalPagesSafe" :key="p" :value="p">{{ p }}</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <MovieCardSkeleton v-for="n in 3" :key="n" />
    </div>
    <div v-else-if="error" class="text-sm text-red-600">Errore: {{ error }}</div>

    <div v-else>
      <div class="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
        <div v-for="m in items" :key="m.id" class="rounded-lg border overflow-hidden bg-white flex flex-col">
          <img
            v-if="m.poster_url"
            :src="m.poster_url"
            alt=""
            class="w-full h-64 object-cover"
            loading="lazy"
          />
          <div class="p-3 space-y-2 flex-1">
            <div class="font-medium line-clamp-2">{{ m.title }}</div>
            <div class="text-xs text-gray-500">Uscita: {{ m.release_date || '—' }}</div>
            <p v-if="m.overview" class="text-xs text-gray-700 line-clamp-3">{{ m.overview }}</p>
          </div>
          <div class="p-3 pt-0 flex justify-end">
            <button
              class="text-sm px-3 py-1.5 rounded bg-green-600 text-white disabled:opacity-60"
              @click="useMovie(m)"
              :disabled="loadingPickId === m.id"
            >
              <span v-if="loadingPickId !== m.id">Usa dati</span>
              <span v-else class="inline-flex items-center gap-1">
                <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4A4 4 0 008 12H4z"/>
                </svg>
                Prendo…
              </span>
            </button>
          </div>
        </div>
      </div>

      <div v-if="totalPagesSafe > 1" class="flex justify-center gap-2 mt-3">
        <button class="px-3 py-1 rounded border" :disabled="page<=1" @click="page--">←</button>
        <div class="text-sm opacity-70 self-center">Pagina {{ page }} / {{ totalPagesSafe }}</div>
        <button class="px-3 py-1 rounded border" :disabled="page>=totalPagesSafe" @click="page++">→</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['prefill'])
const { apiFetch } = useApi()
import MovieCardSkeleton from './MovieCardSkeleton.vue'

const props = defineProps({
  months: { type: Number, default: 3 },
  region: { type: String, default: 'IT' },
  language: { type: String, default: 'it-IT' }
})

const items = ref([])
const loading = ref(false)
const error = ref('')
const page = ref(1)
const totalPages = ref(1)
const loadingPickId = ref(null)

const totalPagesSafe = computed(() => Math.max(1, Math.min(totalPages.value || 1, 10)))

async function fetchUpcoming() {
  loading.value = true
  error.value = ''
  try {
    const res = await apiFetch('/tmdb/upcoming', {
      query: {
        months: String(props.months),
        region: props.region,
        language: props.language,
        page: String(page.value)
      }
    })
    items.value = res.results || []
    totalPages.value = res.total_pages || 1
  } catch (e) {
    console.error(e)
    error.value = e?.response?._data?.detail || 'Errore caricamento TMDb'
  } finally {
    loading.value = false
  }
}

watch([() => props.months, () => props.region, () => props.language, page], fetchUpcoming, { immediate: true })

// Click “Usa dati” → prefill completo con /tmdb/details/{id}
async function useMovie(m) {
  loadingPickId.value = m.id
  try {
    const d = await apiFetch(`/tmdb/details/${m.id}`)
    const payload = {
      title: d?.title || m.title,
      release_date: d?.release_date || m.release_date || null,
      release_year: d?.release_year ?? (m.release_date ? Number(m.release_date.slice(0,4)) : null),
      poster_url: d?.poster_url || m.poster_url || null,
      director: d?.director || null,
      cast: Array.isArray(d?.cast) ? d.cast : [],
      runtime: d?.runtime ?? null,
      tmdb_id: d?.tmdb_id || m.id,
      overview: d?.overview || m.overview || null
    }
    emit('prefill', payload)
  } catch (e) {
    console.error(e)
  } finally {
    loadingPickId.value = null
  }
}
</script>


<style scoped>
.line-clamp-2 { display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.line-clamp-3 { display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical; overflow:hidden; }
</style>
