<!-- components/MovieRowCard.vue -->
<template>
  <article
    class="relative group flex w-full flex-col md:flex-row items-stretch bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:bg-gray-50 dark:hover:bg-gray-700 overflow-hidden transition mb-6"
  >
  <StatusBadge :status="movie.status" />
  <!-- Poster -->

<!-- Poster -->
<div>
  <img
    v-if="movie.poster_url"
    :src="movie.poster_url"
    alt=""
    class="w-full h-64 md:h-72 md:w-48 object-cover rounded"
    loading="lazy"
    decoding="async"
  />
  <div
    v-else
    class="w-full h-64 md:h-72 md:w-48 flex items-center justify-center bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-300 text-xs rounded"
  >
    Nessun poster
  </div>
</div>





    <!-- Contenuto -->
    <div class="flex-1 p-4 flex flex-col gap-3">
      <!-- Stato + Titolo -->
      <div class="flex items-start justify-between gap-3">
        <StatusBadge :status="movie.status" />
        <!-- Pills compatte (score/liked) su desktop le spostiamo in basso, su mobile possono stare qui -->
        <div class="flex md:hidden items-center gap-2 shrink-0">
          <span v-if="movie.score" class="px-2 py-0.5 rounded-full bg-red-600 text-white text-xs">
            Score: <strong>{{ movie.score }}/10</strong>
          </span>
          <span v-if="movie.liked" class="px-2 py-0.5 rounded-full bg-red-600 text-white text-xs">
            {{ likedLabel(movie.liked) }}
          </span>
        </div>
      </div>

      <h3 class="text-xl md:text-2xl font-semibold leading-snug break-words text-black">
        <NuxtLink
          v-if="movie.id"
          :to="`/movies/${movie.id}`"
          class="hover:underline focus:outline-none focus:ring-4 focus:ring-blue-300 rounded-sm"
        >
          {{ movie.title }}
        </NuxtLink>
        <template v-else>{{ movie.title }}</template>
      </h3>

      <!-- Overview (troncata a 3 righe se presente) -->
      <p v-if="movie.overview" class="text-sm text-gray-700 dark:text-gray-300 line-clamp-3">
        {{ movie.overview }}
      </p>

      <!-- Meta -->
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-x-6 gap-y-1 text-sm text-gray-600 dark:text-gray-300">
        <div v-if="movie.release_year"><span class="text-gray-500 dark:text-gray-400">Anno:</span> <span class="font-medium text-gray-900 dark:text-white">{{ movie.release_year }}</span></div>
        <div v-if="movie.release_date"><span class="text-gray-500 dark:text-gray-400">Uscita:</span> <span class="font-medium text-gray-900 dark:text-white">{{ movie.release_date }}</span></div>
        <div v-if="movie.runtime"><span class="text-gray-500 dark:text-gray-400">Durata:</span> <span class="font-medium text-gray-900 dark:text-white">{{ movie.runtime }} min</span></div>
        <div v-if="movie.director"><span class="text-gray-500 dark:text-gray-400">Regia:</span> <span class="font-medium text-gray-900 dark:text-white">{{ movie.director }}</span></div>
        <div v-if="movie.cast?.length" class="col-span-2">
          <span class="text-gray-500 dark:text-gray-400">Cast:</span>
          <span class="font-medium text-gray-900 dark:text-white">{{ movie.cast.slice(0,3).join(', ') }}</span>
        </div>
        <div v-if="movie.tmdb_id" class="col-span-2">
          <span class="text-gray-500 dark:text-gray-400">TMDb:</span>
          <a
            :href="`https://www.themoviedb.org/movie/${movie.tmdb_id}`"
            target="_blank"
            rel="noopener"
            class="text-blue-600 dark:text-blue-400 hover:underline"
          >
            #{{ movie.tmdb_id }}
          </a>
        </div>
      </div>

      <!-- Nota -->
      <div v-if="movie.note" class="text-sm text-gray-700 dark:text-gray-300">
        <span class="text-gray-500 dark:text-gray-400">Nota: </span>{{ movie.note }}
      </div>

      <!-- Pills (desktop) -->
      <div class="hidden md:flex flex-wrap gap-2 mt-1 uppercase">
        <span v-if="movie.score" class="px-2 py-0.5 rounded-full bg-red-600 text-white text-xs">
          Score: <strong>{{ movie.score }}/10</strong>
        </span>
        <span v-if="movie.liked" class="px-2 py-0.5 rounded-full bg-red-600 text-white text-xs">
          {{ likedLabel(movie.liked) }}
        </span>
      </div>

      <!-- Edit form (inline) -->
      <div v-if="editing" class="pt-3 border-t border-gray-200 dark:border-gray-700 mt-2 space-y-3 text-gray-500">
        <div class="grid md:grid-cols-4 gap-3">
          <div class="md:col-span-1">
            <label class="block text-xs font-medium mb-1">Stato</label>
            <select v-model="draft.status" class="w-full border rounded-lg p-2 bg-white dark:bg-gray-800 dark:border-gray-600">
              <option v-for="s in statuses" :key="s.value" :value="s.value">{{ s.label }}</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Score (1–10)</label>
            <input
              v-model.number="draft.score"
              type="number"
              min="1"
              max="10"
              class="w-full border rounded-lg p-2 bg-white dark:bg-gray-800 dark:border-gray-600"
            />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Gradimento</label>
            <select v-model="draft.liked" class="w-full border rounded-lg p-2 bg-white dark:bg-gray-800 dark:border-gray-600">
              <option :value="null">-</option>
              <option v-for="l in likedOptions" :key="l.value" :value="l.value">{{ l.label }}</option>
            </select>
          </div>
          <div class="md:col-span-1"></div>
          <div class="md:col-span-4">
            <label class="block text-xs font-medium mb-1">Nota</label>
            <textarea
              v-model="draft.note"
              rows="3"
              class="w-full border rounded-lg p-2 resize-y bg-white dark:bg-gray-800 dark:border-gray-600"
            ></textarea>
          </div>
        </div>

        <div class="flex justify-end gap-2">
          <button
            @click.stop="save"
            :disabled="loading"
            class="px-4 py-2 text-sm font-medium text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 rounded-lg disabled:opacity-60"
          >
            Salva
          </button>
        </div>
      </div>

      <!-- Footer azioni -->
      <div class="mt-auto pt-2">
        <div class="flex flex-wrap items-center justify-end gap-2">
          <button
            @click.stop="completeFromTmdb"
            :disabled="loading"
            class="text-blue-700 dark:text-blue-400 hover:text-white dark:hover:text-white border border-blue-700 dark:border-blue-500 hover:bg-blue-800 dark:hover:bg-blue-500 focus:ring-4 focus:outline-none focus:ring-blue-300 rounded-lg text-sm px-4 py-2 disabled:opacity-60"
            title="Completa informazioni da TMDb"
          >
            <span v-if="!loading">Completa con TMDb</span>
            <span v-else class="inline-flex items-center gap-2">
              <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4A4 4 0 008 12H4z"/>
              </svg>
              Carico…
            </span>
          </button>

          <button
            @click.stop="toggleEdit"
            :disabled="loading"
            class="text-green-700 dark:text-green-400 hover:text-white dark:hover:text-white border border-green-700 dark:border-green-500 hover:bg-green-800 dark:hover:bg-green-600 focus:ring-4 focus:outline-none focus:ring-green-300 rounded-lg text-sm px-4 py-2 disabled:opacity-60"
          >
            {{ editing ? 'Annulla' : 'Modifica' }}
          </button>

          <button
            @click.stop="remove"
            :disabled="loading"
            class="text-red-700 dark:text-red-400 hover:text-white dark:hover:text-white border border-red-700 dark:border-red-500 hover:bg-red-800 dark:hover:bg-red-600 focus:ring-4 focus:outline-none focus:ring-red-300 rounded-lg text-sm px-4 py-2 disabled:opacity-60"
          >
            Elimina
          </button>
        </div>
      </div>
    </div>
  </article>
</template>

<script setup>
import StatusBadge from '@/components/StatusBadge.vue'

const props = defineProps({
  movie: { type: Object, required: true }
})
const emit = defineEmits(['updated', 'deleted'])

const { apiFetch } = useApi()
const toast = useToast()

const editing = ref(false)
const loading = ref(false)

const draft = reactive({
  status: props.movie.status,
  score: props.movie.score,
  liked: props.movie.liked,
  note: props.movie.note
})

const statuses = [
  { value: 'to_watch', label: 'Da vedere' },
  { value: 'watched',  label: 'Visto' },
  { value: 'upcoming', label: 'In uscita' },
  { value: 'watching', label: 'In visione' }
]

const likedOptions = [
  { value: 'loved',    label: 'Mi è piaciuto molto' },
  { value: 'liked',    label: 'Mi è piaciuto' },
  { value: 'okay',     label: 'Carino' },
  { value: 'disliked', label: 'Non mi è piaciuto' },
  { value: 'terrible', label: 'Pessimo' }
]

function likedLabel(val) {
  return likedOptions.find(l => l.value === val)?.label || val
}

function toggleEdit() {
  editing.value = !editing.value
  if (editing.value) {
    draft.status = props.movie.status
    draft.score  = props.movie.score
    draft.liked  = props.movie.liked
    draft.note   = props.movie.note
  }
}

async function save() {
  const body = {
    status: draft.status,
    score:  draft.score ?? undefined,
    liked:  draft.liked ?? undefined,
    note:   draft.note  ?? undefined
  }
  loading.value = true
  try {
    const updated = await apiFetch(`/movies/${props.movie.id}`, { method: 'PUT', body })
    emit('updated', updated)
    editing.value = false
    toast.show('success', 'Film aggiornato!')
  } catch (e) {
    console.error('Errore aggiornamento film', e)
    toast.show('error', 'Errore durante aggiornamento')
  } finally {
    loading.value = false
  }
}

async function completeFromTmdb() {
  loading.value = true
  try {
    let tmdbId = props.movie.tmdb_id

    if (!tmdbId) {
      const q = window.prompt('Cerca su TMDb:', props.movie.title || '')
      if (!q || !q.trim()) { loading.value = false; return }
      const results = await apiFetch('/tmdb/search', { query: { q: q.trim() } })
      if (!Array.isArray(results) || results.length === 0) {
        toast.show('error', 'Nessun risultato trovato su TMDb.')
        return
      }
      const top = results[0]
      const ok = window.confirm(`Usare "${top.title}" (${top.release_date || '—'})?`)
      if (!ok) return
      tmdbId = top.id
    }

    const details = await apiFetch(`/tmdb/details/${tmdbId}`)
    const body = {
      tmdb_id:      details.tmdb_id ?? tmdbId,
      release_date: details.release_date || undefined,
      release_year: details.release_year ?? undefined,
      poster_url:   details.poster_url || undefined,
      director:     details.director || undefined,
      cast:         Array.isArray(details.cast) ? details.cast : undefined,
      runtime:      details.runtime ?? undefined,
      overview:     details.overview || undefined
    }

    const updated = await apiFetch(`/movies/${props.movie.id}`, { method: 'PUT', body })
    emit('updated', updated)
    toast.show('success', 'Dati completati da TMDb.')
  } catch (e) {
    console.error('TMDb complete error:', e)
    toast.show('error', 'Errore durante il completamento da TMDb.')
  } finally {
    loading.value = false
  }
}

async function remove() {
  if (!confirm(`Vuoi davvero eliminare "${props.movie.title}"?`)) return
  loading.value = true
  try {
    await apiFetch(`/movies/${props.movie.id}`, { method: 'DELETE' })
    emit('deleted', props.movie.id)
    toast.show('success', 'Film eliminato')
  } catch (e) {
    console.error('Errore eliminazione film', e)
    toast.show('error', 'Errore durante l\'eliminazione')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Fallback se non hai il plugin line-clamp di Tailwind */
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
