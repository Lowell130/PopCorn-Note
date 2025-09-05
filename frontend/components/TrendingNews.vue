<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl p-5 shadow">
    <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
      <h2 class="text-xl font-semibold">Novità & Tendenze</h2>

      <div class="flex flex-wrap items-center gap-2">
        <!-- Filtro media -->
        <div class="inline-flex rounded-md shadow-sm" role="group">
          <button
            v-for="m in mediaTabs"
            :key="m.value"
            @click="media = m.value; refetch(true)"
            :class="['px-3 py-1.5 text-sm border', media===m.value
              ? 'bg-blue-600 text-white border-blue-600'
              : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 border-gray-300 dark:border-gray-600 hover:bg-gray-50']"
          >
            {{ m.label }}
          </button>
        </div>

        <!-- Finestra temporale -->
        <div class="inline-flex rounded-md shadow-sm" role="group">
          <button
            v-for="w in windowTabs"
            :key="w.value"
            @click="windowVal = w.value; refetch(true)"
            :class="['px-3 py-1.5 text-sm border', windowVal===w.value
              ? 'bg-purple-600 text-white border-purple-600'
              : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 border-gray-300 dark:border-gray-600 hover:bg-gray-50']"
          >
            {{ w.label }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-sm opacity-70">Caricamento…</div>
    <div v-else-if="error" class="text-sm text-red-600">Errore: {{ error }}</div>
    <div v-else-if="items.length === 0" class="text-sm opacity-70">Nessun risultato.</div>

    <div class="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <article
        v-for="it in items"
        :key="`${it.kind}-${it.id}`"
        class="border rounded-lg overflow-hidden bg-white dark:bg-gray-900 dark:border-gray-700 shadow-sm"
      >
        <div class="relative">
          <img
            v-if="it.poster_url"
            :src="it.poster_url"
            class="w-full aspect-[2/3] object-cover"
            loading="lazy"
          />
          <div v-else class="w-full aspect-[2/3] flex items-center justify-center text-xs text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-800">
            Nessun poster
          </div>

          <span
            class="absolute top-2 left-2 px-2 py-0.5 rounded text-xs font-medium"
            :class="it.kind==='tv'
              ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
              : 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'"
          >
            {{ it.kind==='tv' ? 'SERIE' : 'FILM' }}
          </span>
        </div>

        <div class="p-3 space-y-2">
          <h3 class="text-sm font-semibold leading-tight line-clamp-2">
            <NuxtLink
              :to="it.kind==='tv' ? `/tv/${linkId(it)}` : `/movies/${linkId(it)}`"
              class="hover:underline"
              v-if="it.local_id"
            >
              {{ it.title }}
            </NuxtLink>
            <span v-else>{{ it.title }}</span>
          </h3>

          <p v-if="it.overview" class="text-xs text-gray-600 dark:text-gray-300 line-clamp-3">
            {{ it.overview }}
          </p>

          <div class="flex items-center justify-between text-xs text-gray-500">
            <span v-if="it.release_year">{{ it.release_year }}</span>
            <span v-if="it.vote_average">★ {{ it.vote_average?.toFixed?.(1) ?? it.vote_average }}</span>
          </div>

          <div class="pt-2 flex gap-2">
            <button
              class="px-2 py-1 text-xs rounded border hover:bg-gray-50 dark:hover:bg-gray-800"
              @click="prefill(it)"
              title="Aggiungi alla tua lista"
            >
              Aggiungi
            </button>
            <a
              :href="`https://www.themoviedb.org/${it.kind==='tv'?'tv':'movie'}/${it.tmdb_id}`"
              target="_blank" rel="noopener"
              class="px-2 py-1 text-xs rounded border hover:bg-gray-50 dark:hover:bg-gray-800"
            >
              TMDb
            </a>
          </div>
        </div>
      </article>
    </div>

    <!-- Paginazione semplice -->
    <div class="flex justify-center gap-2 mt-4" v-if="totalPages>1">
      <button
        class="px-3 py-1.5 text-sm rounded border"
        :disabled="page<=1 || loading"
        @click="page--; refetch()"
      >
        « Prec
      </button>
      <span class="text-sm opacity-70 self-center">Pagina {{ page }} / {{ totalPages }}</span>
      <button
        class="px-3 py-1.5 text-sm rounded border"
        :disabled="page>=totalPages || loading"
        @click="page++; refetch()"
      >
        Succ »
      </button>
    </div>
  </section>
</template>

<script setup>
const emit = defineEmits(['prefill']) // per aprire AddMovieForm con dati precompilati
const { apiFetch } = useApi()

// Tabs
const mediaTabs = [
  { value: 'all',   label: 'Tutti' },
  { value: 'movie', label: 'Film' },
  { value: 'tv',    label: 'Serie' },
]
const windowTabs = [
  { value: 'day',  label: 'Oggi' },
  { value: 'week', label: 'Settimana' },
]

// Stato UI
const media = ref('all')
const windowVal = ref('day')
const page = ref(1)

const loading = ref(false)
const error = ref('')
const items = ref([])
const totalPages = ref(1)

// fetch
async function refetch(resetPage = false) {
  if (resetPage) page.value = 1
  loading.value = true
  error.value = ''
  try {
    const data = await apiFetch('/tmdb/trending', {
      query: { media: media.value, window: windowVal.value, page: page.value, language: 'it-IT' }
    })
    items.value = (data?.results || []).map(x => ({ ...x, local_id: null })) // local_id lo useremo se già presente in DB
    totalPages.value = data?.total_pages || 1
  } catch (e) {
    error.value = e?.data?.detail || e?.message || 'Errore'
  } finally {
    loading.value = false
  }
}
onMounted(() => refetch())

// helper: restituisce id locale se in futuro vuoi collegare con i record già salvati
function linkId(it) {
  return it.local_id || it.id
}

// prefill per AddMovieForm
function prefill(it) {
  emit('prefill', {
    title: it.title,
    release_date: it.release_date || null,
    release_year: it.release_year || null,
    poster_url: it.poster_url || null,
    overview: it.overview || null,
    director: null,
    cast: [],
    runtime: null,
    tmdb_id: it.tmdb_id || it.id,
    kind: it.kind || 'movie',
  })
}
</script>

<style scoped>
.line-clamp-2{
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;
}
.line-clamp-3{
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;
}
</style>
