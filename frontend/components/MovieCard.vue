<!-- components/MovieCard.vue -->
<template>
  <div class="relative bg-white text-black rounded-2xl p-5 shadow space-y-4 ">
     <StatusBadge :status="movie.status" />
    <!-- Titolo -->
    <h3 class="text-xl font-semibold break-words">
      <NuxtLink v-if="movie.id" :to="`/movies/${movie.id}`" class="hover:underline">
        {{ movie.title }}
      </NuxtLink>
      <template v-else>{{ movie.title }}</template>
    </h3>
 <!-- <StatusBadge :status="movie.status" /> -->
    <!-- Poster + meta -->
    <div class="flex gap-4 items-start">
      <img
        v-if="movie.poster_url"
        :src="movie.poster_url"
        alt=""
        class="w-24 h-36 rounded object-cover border"
      />
      <div class="text-sm text-gray-700 space-y-1 flex-1">
        <div v-if="movie.release_year">
          <span class="text-gray-500">Anno:</span>
          <span class="text-black font-medium"> {{ movie.release_year }}</span>
        </div>
        <div v-if="movie.release_date">
          <span class="text-gray-500">Uscita:</span>
          <span class="text-black font-medium"> {{ movie.release_date }}</span>
        </div>
        <div v-if="movie.runtime">
          <span class="text-gray-500">Durata:</span>
          <span class="text-black font-medium"> {{ movie.runtime }} min</span>
        </div>
        <div v-if="movie.director">
          <span class="text-gray-500">Regia:</span>
          <span class="text-black font-medium"> {{ movie.director }}</span>
        </div>
        <div v-if="movie.cast?.length">
          <span class="text-gray-500">Cast:</span>
          <span class="text-gray-900">{{ movie.cast.slice(0, 3).join(', ') }}</span>
        </div>
        <div v-if="movie.tmdb_id">
          <span class="text-gray-500">TMDb:</span>
          <a
            :href="`https://www.themoviedb.org/movie/${movie.tmdb_id}`"
            target="_blank"
            rel="noopener"
            class="text-blue-600 hover:underline"
          >
            #{{ movie.tmdb_id }}
          </a>
        </div>
      </div>
    </div>

    <!-- Stato, Score, Gradimento -->
    <div class="flex flex-wrap gap-3">
      <!-- <StatusBadge :status="movie.status" /> -->
      <span v-if="movie.score" class="px-2 py-1 rounded-full bg-gray-100 text-black">
        Score: <strong>{{ movie.score }}/10</strong>
      </span>
      <span v-if="movie.liked" class="px-2 py-1 rounded-full bg-gray-100 text-black">
        Gradimento: <strong>{{ likedLabel(movie.liked) }}</strong>
      </span>
    </div>

    <!-- Nota -->
    <div v-if="movie.note" class="text-sm text-gray-700">
      <p>{{ movie.note }}</p>
    </div>

    <!-- Edit form -->
    <div v-if="editing" class="pt-3 border-t mt-2 space-y-3">
      <div>
        <label for="status" class="block text-xs font-medium">Stato</label>
        <select v-model="draft.status" class="w-full border rounded-lg p-2">
          <option v-for="s in statuses" :key="s.value" :value="s.value">
            {{ s.label }}
          </option>
        </select>
      </div>

      <div>
        <label for="score" class="block text-xs font-medium">Score (1–10)</label>
        <input
          v-model.number="draft.score"
          type="number"
          min="1"
          max="10"
          class="w-full border rounded-lg p-2"
        />
      </div>

      <div>
        <label for="liked" class="block text-xs font-medium">Gradimento</label>
        <select v-model="draft.liked" class="w-full border rounded-lg p-2">
          <option :value="null">-</option>
          <option v-for="l in likedOptions" :key="l.value" :value="l.value">
            {{ l.label }}
          </option>
        </select>
      </div>

      <div>
        <label for="note" class="block text-xs font-medium">Nota</label>
        <textarea
          v-model="draft.note"
          rows="3"
          class="w-full border rounded-lg p-2 resize-y"
        ></textarea>
      </div>

      <div class="flex justify-end">
        <button
          @click="save"
          class="focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5"
          :disabled="loading"
        >
          Salva
        </button>
      </div>
    </div>

    <!-- Azioni (footer centrato) -->
    <div class="pt-3 border-t mt-1">
      <div class="flex flex-wrap items-center justify-center gap-2">
        <button
          @click="completeFromTmdb"
          class="text-blue-700 hover:text-white border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:hover:bg-blue-500 dark:focus:ring-blue-800"
          :disabled="loading"
          title="Completa informazioni (poster, anno, regista, cast) da TMDb"
        >
          <span v-if="!loading">Completa con TMDb</span>
          <span v-else class="inline-flex items-center gap-1">
            <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a 8 8 0 0 1 8-8v4a4 4 0 0 0-4 4H4z"/>
            </svg>
            Carico…
          </span>
        </button>

        <button
          @click="toggleEdit"
          class="text-green-700 hover:text-white border border-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 dark:border-green-500 dark:text-green-500 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-800"
          :disabled="loading"
        >
          {{ editing ? 'Annulla' : 'Modifica' }}
        </button>

        <button
          @click="remove"
         class="text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900"
          :disabled="loading"
        >
          Elimina
        </button>
      </div>
    </div>
  </div>
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
  { value: 'watched', label: 'Visto' },
  { value: 'upcoming', label: 'In uscita' },
  { value: 'watching', label: 'In visione' }
]

const likedOptions = [
  { value: 'loved', label: 'Mi è piaciuto molto' },
  { value: 'liked', label: 'Mi è piaciuto' },
  { value: 'okay', label: 'Carino' },
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
  const payload = {
    status: draft.status,
    score: draft.score ?? undefined,
    liked: draft.liked ?? undefined,
    note:  draft.note  ?? undefined
  }
  loading.value = true
  try {
    const updated = await apiFetch(`/movies/${props.movie.id}`, {
      method: 'PUT',
      body: payload
    })
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

    const payload = {
      tmdb_id: details.tmdb_id ?? tmdbId,
      // title: details.title || undefined,  // scommenta se vuoi aggiornare il titolo
      release_date: details.release_date || undefined,
      release_year: details.release_year ?? undefined,
      poster_url: details.poster_url || undefined,
      director: details.director || undefined,
      cast: Array.isArray(details.cast) ? details.cast : undefined,
      runtime: details.runtime ?? undefined,
      overview: details.overview || undefined,          // 👈 aggiunto
    }

    const updated = await apiFetch(`/movies/${props.movie.id}`, {
      method: 'PUT',
      body: payload
    })
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
