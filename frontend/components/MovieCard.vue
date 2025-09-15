<!-- components/MovieRowCard.vue -->
<template>
  <article :class="cardClasses">
    <div class="text-gray-800 rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800 w-full">
   <div class="w-full aspect-[2/3] overflow-hidden rounded">
 
   <NuxtLink
            v-if="movie.id"
            :to="movie.kind === 'tv' ? `/tv/${movie.id}` : `/movies/${movie.id}`"
            class="hover:underline focus:outline-none focus:ring-4 focus:ring-blue-300 rounded-sm"
          >
       
        
 
    <img
    v-if="movie.poster_url"
    :src="movie.poster_url"
    alt=""
    class="w-full h-full object-cover"
    loading="lazy"
    decoding="async"
  />
    </NuxtLink>
  <div v-else class="w-full h-full flex items-center justify-center text-xs text-gray-500 bg-gray-100">
    Nessun poster
  </div>
</div>

      <div class="pt-4">
        <div class="mb-4 flex items-center justify-between gap-4">
          <span v-if="movie.kind" :class="kindChipClass">
            {{ kindLabel }}
          </span>
          <StatusBadge :status="movie.status" />
        </div>

        <h3 class="text-lg font-semibold leading-snug break-words text-black">
          <NuxtLink
            v-if="movie.id"
            :to="movie.kind === 'tv' ? `/tv/${movie.id}` : `/movies/${movie.id}`"
            class="hover:underline focus:outline-none focus:ring-4 focus:ring-blue-300 rounded-sm"
          >
            {{ shortTitle }}
          </NuxtLink>
          <template v-else>{{ shortTitle }}</template>
        </h3>

        <ul class="mt-3 flex items-center gap-4 text-sm text-gray-600">
          <li v-if="movie.director" class="flex items-center gap-2">
            <svg class="h-4 w-4 text-gray-400" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13 7h6l2 4m-8-4v8m0-8V6a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v9h2m8 0H9m4 0h2m4 0h2v-4m0 0h-5"/>
            </svg>
           <a :href="directorUrl" class="font-medium text-blue-700 hover:underline">
  {{ movie.director ? (movie.director.length > 10 ? movie.director.slice(0, 10) + '…' : movie.director) : '' }}
</a>
          </li>
          <li v-if="movie.release_year" class="flex items-center gap-2">
            <svg class="h-4 w-4 text-gray-400" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path stroke="currentColor" stroke-linecap="round" stroke-width="2"
                    d="M8 7V6c0-.6.4-1 1-1h11c.6 0 1 .4 1 1v7c0 .6-.4 1-1 1h-1M3 18v-7c0-.6.4-1 1-1h11c.6 0 1 .4 1 1v7c0 .6-.4 1-1 1H4a1 1 0 0 1-1-1Z"/>
            </svg>
            {{ movie.release_year }}
          </li>
        </ul>

        










        

        <div class="mt-4 flex items-center justify-between gap-4">
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
 <Transition
  enter-active-class="transition duration-200 ease-out"
  enter-from-class="opacity-0 -translate-y-2"
  enter-to-class="opacity-100 translate-y-0"
  leave-active-class="transition duration-150 ease-in"
  leave-from-class="opacity-100 translate-y-0"
  leave-to-class="opacity-0 -translate-y-2"
>
  <div v-if="editing" class="mt-4 -mx-6 border-t border-gray-200">
    <div class="bg-gray-50/80 backdrop-blur-sm px-6 py-4 space-y-3">
      <!-- TUTTO A COLONNA -->
      <div>
        <label class="block text-xs font-medium mb-1 text-gray-600">Stato</label>
        <select
          v-model="draft.status"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        >
          <option v-for="s in statuses" :key="s.value" :value="s.value">{{ s.label }}</option>
        </select>
      </div>

      <div>
        <label class="block text-xs font-medium mb-1 text-gray-600">Score (1–10)</label>
        <input
          v-model.number="draft.score"
          type="number"
          min="1"
          max="10"
          inputmode="numeric"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        />
      </div>

      <div>
        <label class="block text-xs font-medium mb-1 text-gray-600">Gradimento</label>
        <select
          v-model="draft.liked"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        >
          <option :value="null">—</option>
          <option v-for="l in likedOptions" :key="l.value" :value="l.value">{{ l.label }}</option>
        </select>
      </div>

      <div>
        <label class="block text-xs font-medium mb-1 text-gray-600">Nota</label>
        <textarea
          v-model="draft.note"
          rows="4"
               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-">Nota</label>

        ></textarea>
      </div>

      <!-- Footer azioni -->
      <div class="pt-1 flex justify-end gap-2">
        <button
          @click.stop="toggleEdit"
          type="button"
          class="px-4 py-2 text-sm font-medium rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300"
        >
          Annulla
        </button>
        <button
          @click.stop="save"
          :disabled="loading"
          type="button"
          class="px-4 py-2 text-sm font-medium rounded-lg text-white bg-green-700 hover:bg-green-800 focus:outline-none focus:ring-2 focus:ring-green-300 disabled:opacity-60"
        >
          Salva
        </button>
      </div>
    </div>
  </div>
</Transition>

    </div>
  </article>
</template>

<script setup>
import StatusBadge from '@/components/StatusBadge.vue'

const props = defineProps({ movie: { type: Object, required: true } })
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

const likedOptions = [
  { value: 'loved',    label: 'Mi è piaciuto molto' },
  { value: 'liked',    label: 'Mi è piaciuto' },
  { value: 'okay',     label: 'Carino' },
  { value: 'disliked', label: 'Non mi è piaciuto' },
  { value: 'terrible', label: 'Pessimo' }
]

const kindLabel = computed(() => props.movie.kind === 'tv' ? 'SERIE' : 'FILM')
const kindChipClass = computed(() =>
  props.movie.kind === 'tv'
    ? 'bg-yellow-100 text-yellow-800 text-xs font-medium px-2.5 py-0.5 rounded'
    : 'bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded'
)

const isWatched = computed(() => props.movie.status === 'watched')
const cardClasses = computed(() => [
  // wrapper esterno (non grid)
  'w-full',
  isWatched.value ? 'grayscale opacity-80 hover:grayscale-0 hover:opacity-100 transition' : ''
])

const shortTitle = computed(() => {
  const t = props.movie.title || ''
  return t.length > 23 ? t.slice(0, 23) + '…' : t
})

const directorUrl = computed(() => {
  const name = props.movie.director
  const id = props.movie.director_id
  if (id) return `https://www.themoviedb.org/person/${id}`
  const q = encodeURIComponent(name || '')
  return `https://www.themoviedb.org/search?query=${q}`
})

function toggleEdit() {
  editing.value = !editing.value
  if (editing.value) {
    draft.status = props.movie.status
    draft.score  = props.movie.score
    draft.liked  = props.movie.liked
    draft.note   = props.movie.note
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
    console.error(e)
    toast.show('error', 'Errore durante l\'eliminazione')
  } finally {
    loading.value = false
  }
}

// Opzioni "Stato" — MANCAVANO
const statuses = [
  { value: 'to_watch', label: 'Da vedere' },
  { value: 'watched',  label: 'Visto' },
  { value: 'upcoming', label: 'In uscita' },
  { value: 'watching', label: 'In visione' },
]

// Salvataggio — MANCAVA
async function save() {
  // normalizza score ('' -> null) e liked (stringa o null)
  const score =
    draft.score === '' || draft.score == null
      ? null
      : Math.max(1, Math.min(10, Number(draft.score)))

  const body = {
    status: draft.status,
    score:  score ?? undefined,          // undefined => non tocca il campo
    liked:  draft.liked ?? undefined,
    note:   (draft.note ?? '').trim() || undefined,
  }

  loading.value = true
  try {
    const updated = await apiFetch(`/movies/${props.movie.id}`, {
      method: 'PUT',
      body,
    })
    emit('updated', updated)
    editing.value = false
    toast.show?.('success', 'Salvato!')
  } catch (e) {
    console.error('save error', e)
    toast.show?.('error', 'Errore durante il salvataggio')
  } finally {
    loading.value = false
  }
}
</script>
