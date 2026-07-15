<!-- components/TrendingNews.vue -->
<template>
  <section class="bg-transparent text-white space-y-6">
    <div class="flex flex-col items-center gap-3 mb-6">
      <div class="flex flex-wrap items-center justify-center gap-2 select-none">

        <!-- Filtro media -->
        <div class="inline-flex rounded-xl bg-white/5 border border-white/10 p-0.5" role="group">
          <button
            v-for="(m, idx) in mediaTabs"
            :key="m.value"
            @click="media = m.value; refetch(true)"
            type="button"
            :class="[
              'px-4 py-2 text-xs font-semibold cursor-pointer transition-all duration-150',
              idx === 0 ? 'rounded-l-xl' : idx === mediaTabs.length - 1 ? 'rounded-r-xl' : '',
              media === m.value
                ? 'text-sky-300 bg-sky-500/10 border-r border-transparent'
                : 'text-gray-400 hover:text-white hover:bg-white/5'
            ]"
          >
            {{ m.label }}
          </button>
        </div>

        <!-- Finestra temporale -->
        <div class="inline-flex rounded-xl bg-white/5 border border-white/10 p-0.5" role="group">
          <button
            v-for="(w, idx) in windowTabs"
            :key="w.value"
            @click="windowVal = w.value; refetch(true)"
            type="button"
            :class="[
              'px-4 py-2 text-xs font-semibold cursor-pointer transition-all duration-150',
              idx === 0 ? 'rounded-l-xl' : idx === windowTabs.length - 1 ? 'rounded-r-xl' : '',
              windowVal === w.value
                ? 'text-purple-300 bg-purple-500/10'
                : 'text-gray-400 hover:text-white hover:bg-white/5'
            ]"
          >
            {{ w.label }}
          </button>
        </div>

      </div>
    </div>

    <!-- Skeletons Loading -->
    <div v-if="loading" class="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
       <MovieCardSkeleton v-for="n in 8" :key="n" />
    </div>
    <div v-else-if="error" class="text-sm text-red-400 font-semibold">Errore: {{ error }}</div>
    <div v-else-if="items.length === 0" class="text-sm text-gray-500">Nessun risultato.</div>

    <!-- Items Grid -->
    <div v-else class="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 animate-fade-in-up">
      <article
        v-for="it in items"
        :key="`${it.kind}-${it.id}`"
        class="text-white rounded-2xl bg-white/5 border border-white/10 p-4 shadow-lg backdrop-blur-sm w-full h-full flex flex-col justify-between"
      >
        <div class="space-y-4">
          <div class="relative overflow-hidden rounded-xl aspect-[2/3]">
            <img
              v-if="it.poster_url"
              :src="it.poster_url"
              class="w-full h-full object-cover transition duration-300 hover:scale-105"
              loading="lazy"
            />
            <div v-else class="w-full h-full flex items-center justify-center text-xs text-gray-500 bg-white/5 border border-white/5">
              Nessun poster
            </div>

            <span
              class="absolute top-2 left-2 px-2.5 py-0.5 rounded-md text-[10px] font-bold shadow-sm"
              :class="it.kind==='tv'
                ? 'bg-yellow-500/20 border border-yellow-500/30 text-yellow-300'
                : 'bg-blue-500/20 border border-blue-500/30 text-blue-300'"
            >
              {{ it.kind==='tv' ? 'SERIE' : 'FILM' }}
            </span>
          </div>

          <div class="space-y-2">
            <h3 class="text-md font-bold leading-snug break-words text-white hover:text-purple-400 transition-colors">
              <NuxtLink
                v-if="it.local_id"
                :to="it.kind==='tv' ? `/tv/${it.local_id}` : `/movies/${it.local_id}`"
                class="hover:underline"
              >
                {{ it.title.length > 25 ? it.title.slice(0, 25) + '...' : it.title }}
              </NuxtLink>
              <span v-else>{{ it.title.length > 25 ? it.title.slice(0, 25) + '...' : it.title }}</span>
            </h3>

            <p class="text-xs text-gray-400 line-clamp-3 leading-relaxed">
              {{ it.overview || 'N/A' }}
            </p>

            <div class="flex items-center justify-between text-xs text-gray-500">
              <span v-if="it.release_year">{{ it.release_year }}</span>
              <span v-if="it.vote_average" class="flex items-center gap-0.5 text-amber-400">★ {{ toOne(it.vote_average) }}</span>
            </div>
          </div>
        </div>

        <!-- Azioni Card -->
        <div class="mt-4 flex items-center justify-between gap-2 border-t border-white/5 pt-3">
          <button
            v-if="!it.local_id"
            class="text-green-300 bg-green-500/10 border border-green-500/20 hover:bg-green-500/20 focus:outline-none rounded-xl text-xs font-semibold px-3 py-2 disabled:opacity-60 cursor-pointer shadow-sm shadow-green-500/5"
            :disabled="addingKey === keyOf(it)"
            @click="quickAdd(it)"
            title="Aggiungi alla tua lista"
          >
            <span v-if="addingKey !== keyOf(it)">+ Aggiungi</span>
            <span v-else class="inline-flex items-center gap-1">
              <svg class="animate-spin h-3 w-3" viewBox="0 0 24 24" fill="none">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4A4 4 0 008 12H4z"/>
              </svg>
              Salvo…
            </span>
          </button>

          <NuxtLink
            v-else
            :to="it.kind==='tv' ? `/tv/${it.local_id}` : `/movies/${it.local_id}`"
            class="text-green-400 bg-green-500/10 border border-green-500/20 font-semibold rounded-xl text-xs px-3 py-2 inline-flex items-center gap-1 shadow-sm shadow-green-500/5"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path>
            </svg>
            In Lista
          </NuxtLink>

          <a
            :href="`https://www.themoviedb.org/${it.kind==='tv'?'tv':'movie'}/${it.tmdb_id}`"
            target="_blank"
            rel="noopener"
            class="text-gray-300 bg-white/5 border border-white/10 hover:bg-white/10 rounded-xl text-xs font-semibold px-4 py-2 transition"
          >
            TMDb
          </a>
        </div>
      </article>
    </div>

    <!-- Paginazione Avanzata -->
    <div class="flex justify-center items-center gap-2 mt-8 select-none" v-if="totalPages > 1">
      
      <!-- Previous -->
      <button
        type="button"
        class="flex items-center justify-center px-4 py-2 text-xs font-semibold text-gray-300 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 disabled:opacity-40 disabled:cursor-not-allowed transition cursor-pointer shadow-md"
        :disabled="page <= 1 || loading"
        @click="goPrev()"
      >
        <svg class="w-3 h-3 me-2" aria-hidden="true" fill="none" viewBox="0 0 14 10" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 5H1m0 0L5 9M1 5l4-4"/>
        </svg>
        Prec
      </button>

      <!-- Page Numbers -->
      <div class="hidden sm:flex items-center gap-1.5">
        <template v-for="(p, idx) in visiblePages" :key="idx">
          <span
            v-if="p === '...'"
            class="px-3 py-2 text-xs font-semibold text-gray-500 cursor-default"
          >
            ...
          </span>
          <button
            v-else
            type="button"
            @click="goToPage(p)"
            :class="[
              'px-3 py-2 text-xs font-semibold rounded-xl transition cursor-pointer',
              page === p
                ? 'text-purple-300 bg-purple-500/20 border border-purple-500/40 shadow-lg shadow-purple-500/5'
                : 'text-gray-300 bg-white/5 border border-white/10 hover:bg-white/10'
            ]"
          >
            {{ p }}
          </button>
        </template>
      </div>

      <!-- Mobile Indicator -->
      <span class="sm:hidden text-xs text-gray-400 font-medium">
        {{ page }} / {{ totalPages }}
      </span>

      <!-- Next -->
      <button
        type="button"
        class="flex items-center justify-center px-4 py-2 text-xs font-semibold text-gray-300 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 disabled:opacity-40 disabled:cursor-not-allowed transition cursor-pointer shadow-md"
        :disabled="page >= totalPages || loading"
        @click="goNext()"
      >
        Succ
        <svg class="w-3 h-3 ms-2" aria-hidden="true" fill="none" viewBox="0 0 14 10" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
      </button>

    </div>
  </section>
</template>

<script setup>
import MovieCardSkeleton from './MovieCardSkeleton.vue'

const { apiFetch } = useApi()
const toast = useToast?.()

// Tabs
const mediaTabs = [
  { value: 'all',   label: 'Tutti' },
  { value: 'movie', label: 'Film' },
  { value: 'tv',    label: 'Serie TV' },
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

const addingKey = ref(null)

// utils
function keyOf(it){ return `${it.kind}-${it.id}` }
function toOne(n){
  const x = typeof n === 'number' ? n : Number(n)
  return Number.isFinite(x) ? x.toFixed(1) : n
}

// fetch
async function refetch(resetPage = false) {
  if (resetPage) page.value = 1
  loading.value = true
  error.value = ''
  try {
    const data = await apiFetch('/tmdb/trending', {
      query: { media: media.value, window: windowVal.value, page: page.value, language: 'it-IT' }
    })
    items.value = (data?.results || []).map(x => ({ ...x, local_id: x.local_id ?? null }))
    totalPages.value = data?.total_pages || 1
  } catch (e) {
    error.value = e?.data?.detail || e?.message || 'Errore'
  } finally {
    loading.value = false
  }
}
onMounted(() => refetch())

// Aggiunta rapida
async function quickAdd(it) {
  addingKey.value = keyOf(it)
  try {
    const details = await apiFetch(it.kind === 'tv' ? `/tmdb/tv/${it.id}` : `/tmdb/details/${it.id}`)
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
      overview: details.overview || null,
      tmdb_vote: details.vote_average ?? it.vote_average ?? null,
    }
    const saved = await apiFetch('/movies/', { method: 'POST', body })
    const idx = items.value.findIndex(x => keyOf(x) === keyOf(it))
    if (idx !== -1) items.value[idx].local_id = saved.id

    toast?.show?.('success', `"${saved.title}" aggiunto!`)
  } catch (e) {
    console.error('quickAdd trending error', e)
    if (e?.response?.status === 409) {
      toast?.show?.('error', 'Questo titolo è già presente nella tua collezione!')
    } else {
      toast?.show?.('error', 'Errore durante l\'aggiunta')
    }
  } finally {
    addingKey.value = null
  }
}

function scrollToTopSmooth() {
  if (typeof window !== 'undefined') {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

async function goPrev() {
  if (page.value <= 1 || loading.value) return
  page.value = Math.max(1, page.value - 1)
  await refetch()
  scrollToTopSmooth()
}

async function goNext() {
  if (page.value >= totalPages.value || loading.value) return
  page.value = Math.min(totalPages.value, page.value + 1)
  await refetch()
  scrollToTopSmooth()
}

async function goToPage(p) {
  if (p === page.value || loading.value) return
  page.value = p
  await refetch()
  scrollToTopSmooth()
}

const visiblePages = computed(() => {
  const total = totalPages.value
  const current = page.value
  const delta = 1
  const range = []
  const rangeWithDots = []
  let l

  for (let i = 1; i <= total; i++) {
    if (i === 1 || i === total || (i >= current - delta && i <= current + delta)) {
      range.push(i)
    }
  }

  for (let i of range) {
    if (l) {
      if (i - l === 2) {
        rangeWithDots.push(l + 1)
      } else if (i - l !== 1) {
        rangeWithDots.push('...')
      }
    }
    rangeWithDots.push(i)
    l = i
  }
  return rangeWithDots
})
</script>
