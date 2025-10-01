<template>
  <section v-if="tmdbId" class="mt-6">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-lg font-semibold text-black">Correlati</h3>

      <!-- Paginazione semplice -->
      <div v-if="totalPages > 1" class="flex items-center gap-2">
        <button
          type="button"
          class="px-3 py-1.5 text-sm rounded border disabled:opacity-50"
          :disabled="page<=1 || loading"
          @click="page--; load()"
        >« Prec</button>
        <span class="text-sm opacity-70">Pagina {{ page }} / {{ totalPages }}</span>
        <button
          type="button"
          class="px-3 py-1.5 text-sm rounded border disabled:opacity-50"
          :disabled="page>=totalPages || loading"
          @click="page++; load()"
        >Succ »</button>
      </div>
    </div>

    <div v-if="loading" class="text-sm opacity-70">Caricamento correlati…</div>
    <div v-else-if="error" class="text-sm text-red-600">Errore: {{ error }}</div>
    <div v-else-if="items.length === 0" class="text-sm opacity-70">Nessun elemento correlato.</div>

    <div class="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <article
        v-for="it in items"
        :key="`${it.kind}-${it.id}`"
        class="border rounded-lg overflow-hidden bg-white shadow-sm"
      >
        <div class="relative">
          <img
            v-if="it.poster_url"
            :src="it.poster_url"
            class="w-full aspect-[2/3] object-cover"
            loading="lazy"
          />
          <div v-else class="w-full aspect-[2/3] flex items-center justify-center text-xs text-gray-500 bg-gray-100">
            Nessun poster
          </div>

          <span
            class="absolute top-2 left-2 px-2 py-0.5 rounded text-xs font-medium shadow-sm"
            :class="it.kind==='tv' ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-100 text-blue-800'"
          >
            {{ it.kind==='tv' ? 'SERIE' : 'FILM' }}
          </span>
        </div>

        <div class="p-3 space-y-2">
            <h3 class="text-md font-semibold leading-snug break-words text-black">
          {{ it.title.length > 25 ? it.title.slice(0, 25) + '...' : it.title }}
          </h3>

          <p v-if="it.overview" class="text-xs text-gray-600 line-clamp-3">{{ it.overview }}</p>

          <div class="flex items-center justify-between text-xs text-gray-500">
            <span v-if="it.release_year">{{ it.release_year }}</span>
            <span v-if="it.vote_average">★ {{ toOne(it.vote_average) }}</span>
          </div>

            <div class="mt-4 flex items-center justify-between gap-4">
            <button
              class="text-green-700 hover:text-white border border-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 rounded-lg text-sm px-4 py-2 disabled:opacity-60"
              :disabled="addingKey === keyOf(it)"
              @click="quickAdd(it)"
              title="Aggiungi alla tua lista"
            >
              <span v-if="addingKey !== keyOf(it)">Aggiungi</span>
              <span v-else class="inline-flex items-center gap-1">
                <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4A4 4 0 008 12H4z"/>
                </svg>
                Salvo…
              </span>
            </button>

            <a type="button"
              :href="`https://www.themoviedb.org/${it.kind==='tv'?'tv':'movie'}/${it.tmdb_id}`"
              target="_blank"
              rel="noopener"
              class="text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700"
            >
              TMDB
            </a>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  kind: { type: String, required: true },      // 'movie' | 'tv'
  tmdbId: { type: Number, required: true }
})

const { apiFetch } = useApi()
const toast = useToast?.() // se non usi il tuo composable toast, sostituisci con alert

const items = ref([])
const page = ref(1)
const totalPages = ref(1)
const loading = ref(false)
const error = ref('')
const addingKey = ref(null)

function keyOf(it) {
  return `${it.kind}-${it.id}`
}
function toOne(n) {
  const x = typeof n === 'number' ? n : Number(n)
  if (Number.isFinite(x)) return x.toFixed(1)
  return n
}


async function load() {
  loading.value = true
  error.value = ''
  try {
    const path = props.kind === 'movie'
      ? `/tmdb/movie/${props.tmdbId}/recommendations`
      : `/tmdb/tv/${props.tmdbId}/recommendations`
    const data = await apiFetch(path, { query: { page: page.value, language: 'it-IT' } })
    items.value = data?.results || []
    totalPages.value = data?.total_pages || 1
  } catch (e) {
    error.value = e?.response?._data?.detail || e?.message || 'Errore'
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => props.tmdbId, () => { page.value = 1; load() })

// Aggiunta rapida nel DB: prende i dettagli e fa POST /movies
async function quickAdd(it) {
  addingKey.value = keyOf(it)
  try {
    const details = await apiFetch(it.kind === 'movie' ? `/tmdb/details/${it.id}` : `/tmdb/tv/${it.id}`)

    const body = {
      kind: details.kind || it.kind,
      title: details.title,
      status: 'to_watch',
      release_date: details.release_date || null,
      release_year: details.release_year ?? null,
      poster_url: details.poster_url || null,
      director: details.director || null,
      cast: Array.isArray(details.cast) ? details.cast : null,
      runtime: details.runtime ?? null,
      tmdb_id: details.tmdb_id || it.id,
      overview: details.overview || null
    }

    const saved = await apiFetch('/movies/', { method: 'POST', body })
    // feedback
    if (toast?.show) toast.show('success', `"${saved.title}" aggiunto!`)
    else alert(`"${saved.title}" aggiunto!`)
  } catch (e) {
    console.error('quickAdd error', e)
    if (toast?.show) toast.show('error', 'Errore durante aggiunta')
    else alert('Errore durante aggiunta')
  } finally {
    addingKey.value = null
  }
}
</script>

<style scoped>
.line-clamp-2{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.line-clamp-3{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
</style>
