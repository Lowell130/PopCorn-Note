<!-- components/MovieRowCard.vue -->
<!-- components/MovieRowCard.vue -->
<template>
  <article :class="cardClasses">
    <!-- ribbon 'VISTO' -->
    <!-- <div
      v-if="isWatched"
      class="absolute top-2 right-2 z-10 inline-flex items-center gap-1 rounded-full bg-purple-600/90 text-white text-[11px] font-medium px-2.5 py-0.5 shadow"
      aria-label="Visto"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 0 1 0 1.414l-7.25 7.25a1 1 0 0 1-1.414 0l-3-3a1 1 0 1 1 1.414-1.414l2.293 2.293 6.543-6.543a1 1 0 0 1 1.414 0z" clip-rule="evenodd"/>
      </svg>
      VISTO
    </div> -->

    <!-- Poster -->
    <div>
      <img
        v-if="movie.poster_url"
        :src="movie.poster_url"
        alt=""
        class="w-full h-56 md:h-64 md:w-40 object-cover rounded"
        loading="lazy"
        decoding="async"
      />
      <div
        v-else
        class="w-full h-56 md:h-64 md:w-40 flex items-center justify-center bg-gray-100 text-gray-500 text-xs rounded"
      >
        Nessun poster
      </div>
    </div>

    <!-- Contenuto -->
    <div class="flex-1 p-4 flex flex-col gap-3">
      <!-- Stato + Titolo -->
      <div class="flex items-start justify-between gap-3">
        <StatusBadge :status="movie.status" />
        <!-- Pills compatte (solo mobile) -->
        <div class="flex md:hidden items-center gap-2 shrink-0">
          <span v-if="movie.score" class="px-2 py-0.5 rounded-full bg-red-600 text-white text-xs">
            Score: <strong>{{ movie.score }}/10</strong>
          </span>
          <span v-if="movie.liked" class="px-2 py-0.5 rounded-full bg-red-600 text-white text-xs">
            {{ likedLabel(movie.liked) }}
          </span>
        </div>
      </div>

      <!-- Titolo + etichetta FILM/SERIE -->
      <h3 class="text-xl md:text-2xl font-semibold leading-snug break-words text-black">
        <div class="flex items-center gap-2">
          <span v-if="movie.kind" :class="kindChipClass">{{ kindLabel }}</span>
          <NuxtLink
            v-if="movie.id"
            :to="movie.kind === 'tv' ? `/tv/${movie.id}` : `/movies/${movie.id}`"
            class="hover:underline focus:outline-none focus:ring-4 focus:ring-blue-300 rounded-sm"
          >
            {{ shortTitle }}
          </NuxtLink>
          <template v-else>{{ shortTitle }}</template>
        </div>
      </h3>

      <!-- Overview (max 110 caratteri) -->
      <p v-if="movie.overview" class="text-sm text-gray-700">
        {{ shortOverview }}
      </p>

      <!-- Meta -->
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-x-6 gap-y-1 text-sm text-gray-600">
        <div v-if="movie.release_year">
          <span class="text-gray-500">Anno:</span>
          <span class="font-medium text-gray-900"> {{ movie.release_year }}</span>
        </div>
        <div v-if="movie.release_date">
          <span class="text-gray-500">Uscita:</span>
          <span class="font-medium text-gray-900"> {{ movie.release_date }}</span>
        </div>
        <div v-if="movie.runtime">
          <span class="text-gray-500">Durata:</span>
          <span class="font-medium text-gray-900"> {{ movie.runtime }} min</span>
        </div>



       <div v-if="movie.director">
  <span class="text-gray-500">Regia:</span>
  <a
    :href="directorUrl"
    target="_blank"
    rel="noopener"
    class="font-medium text-blue-700 hover:underline"
    :title="`Apri ${movie.director} su TMDb`"
  >
    {{ movie.director }}
  </a>
</div>




        <div v-if="movie.cast?.length" class="col-span-2">
          <span class="text-gray-500">Cast:</span>
          <span class="font-medium text-gray-900">{{ movie.cast.slice(0,3).join(', ') }}</span>
        </div>
        <div v-if="movie.tmdb_id" class="col-span-2">
          <span class="text-gray-500">TMDb:</span>
          <a
            :href="`https://www.themoviedb.org/${movie.kind === 'tv' ? 'tv' : 'movie'}/${movie.tmdb_id}`"
            target="_blank" rel="noopener"
            class="text-blue-600 hover:underline"
          >
            #{{ movie.tmdb_id }}
          </a>
        </div>
      </div>

      <!-- Nota -->
      <div v-if="movie.note" class="text-sm text-gray-700">
        <span class="text-gray-500">Nota: </span>{{ movie.note }}
      </div>

      <!-- BOTTOM BAR: pills + azioni (desktop) -->
      <div class="mt-auto pt-2">
        <div class="hidden md:flex items-center justify-between gap-2 flex-wrap">
          <!-- Pills a sinistra -->
          <div class="flex flex-wrap gap-2 uppercase">
            <span v-if="movie.score" class="px-2 py-0.5 rounded-full bg-red-600 text-white text-xs">
              Score: <strong>{{ movie.score }}/10</strong>
            </span>
            <span v-if="movie.liked" class="px-2 py-0.5 rounded-full bg-red-600 text-white text-xs">
              {{ likedLabel(movie.liked) }}
            </span>
          </div>

          <!-- Azioni a destra -->
          <div class="flex items-center gap-2">
            <button
              @click.stop="toggleEdit"
              :disabled="loading"
              class="text-green-700 hover:text-white border border-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 rounded-lg text-sm px-4 py-2 disabled:opacity-60"
            >
              {{ editing ? 'Annulla' : 'Modifica' }}
            </button>

            <button
              @click.stop="remove"
              :disabled="loading"
              class="text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 rounded-lg text-sm px-4 py-2 disabled:opacity-60"
            >
              Elimina
            </button>
          </div>
        </div>

        <!-- Variante mobile: solo azioni (le pills restano in alto) -->
        <div class="md:hidden flex flex-wrap items-center justify-end gap-2">
          <button
            @click.stop="toggleEdit"
            :disabled="loading"
            class="text-green-700 hover:text-white border border-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 rounded-lg text-sm px-4 py-2 disabled:opacity-60"
          >
            {{ editing ? 'Annulla' : 'Modifica' }}
          </button>

          <button
            @click.stop="remove"
            :disabled="loading"
            class="text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 rounded-lg text-sm px-4 py-2 disabled:opacity-60"
          >
            Elimina
          </button>
        </div>
      </div>

      <!-- Edit form (inline) -->
      <div v-if="editing" class="pt-3 border-t border-gray-200 mt-2 space-y-3 text-gray-500">
        <div class="grid md:grid-cols-4 gap-3">
          <div class="md:col-span-1">
            <label class="block text-xs font-medium mb-1">Stato</label>
            <select v-model="draft.status" class="w-full border rounded-lg p-2 bg-white">
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
              class="w-full border rounded-lg p-2 bg-white"
            />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Gradimento</label>
            <select v-model="draft.liked" class="w-full border rounded-lg p-2 bg-white">
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
              class="w-full border rounded-lg p-2 resize-y bg-white"
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
    </div>
  </article>
</template>


<script setup>
import StatusBadge from '@/components/StatusBadge.vue'


const directorUrl = computed(() => {
  const name = props.movie.director
  const id = props.movie.director_id   // se in futuro lo salvi nel DB
  if (id) return `https://www.themoviedb.org/person/${id}`
  // fallback: ricerca generale su TMDb
  const q = encodeURIComponent(name || '')
  return `https://www.themoviedb.org/search?query=${q}`
})


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

const shortOverview = computed(() => {
  const t = props.movie.overview || ''
  return t.length > 110 ? t.slice(0, 110) + '…' : t
})

const kindLabel = computed(() => props.movie.kind === 'tv' ? 'SERIE' : 'FILM')
const kindChipClass = computed(() =>
  props.movie.kind === 'tv'
    ? 'bg-yellow-100 text-yellow-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm'
    : 'bg-blue-100 text-blue-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm'
)

// 👇 nuovo: stile “visto”
const isWatched = computed(() => props.movie.status === 'watched')
const cardClasses = computed(() => [
  'relative group flex w-full flex-col md:flex-row items-stretch bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-50 overflow-hidden transition mb-6',
  // quando visto: spegni colori e abbassa opacità, ripristina al hover
  isWatched.value
    ? 'grayscale opacity-70 hover:grayscale-0 hover:opacity-100'
    : ''
])

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

// Titolo abbreviato (max 40 caratteri)
const shortTitle = computed(() => {
  const t = props.movie.title || ''
  return t.length > 40 ? t.slice(0, 40) + '…' : t
})

</script>

<style scoped>
/* Fallback per line-clamp non più usato qui */
</style>
