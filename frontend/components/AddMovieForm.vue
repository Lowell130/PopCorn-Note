<template>
  <form @submit.prevent="submit" class="bg-white text-black rounded-2xl p-5 shadow space-y-4">
    <h2 class="text-lg font-semibold">Aggiungi un film</h2>

    <!-- Titolo + Poster -->
    <div class="grid md:grid-cols-3 gap-3">
      <div class="md:col-span-2">
        <label class="block mb-1 text-sm font-medium">
          Titolo <span class="text-red-600">*</span>
        </label>
        <input v-model.trim="form.title" type="text" class="w-full border rounded-lg p-2" required />
      </div>
      <div class="flex items-end">
        <div class="w-full">
          <label class="block mb-1 text-sm font-medium">Poster URL</label>
          <input v-model.trim="form.poster_url" type="text" class="w-full border rounded-lg p-2" placeholder="https://..." />
          <div v-if="form.poster_url" class="mt-2">
            <img :src="form.poster_url" alt="poster" class="h-32 rounded object-cover border" />
          </div>
        </div>
      </div>
    </div>

    <!-- Status / Score / Liked -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
      <div>
        <label class="block mb-1 text-sm font-medium">Stato</label>
        <select v-model="form.status" class="w-full border rounded-lg p-2">
          <option v-for="s in statuses" :key="s.value" :value="s.value">{{ s.label }}</option>
        </select>
      </div>
      <div>
        <label class="block mb-1 text-sm font-medium">Score (1–10)</label>
        <input v-model.number="form.score" type="number" min="1" max="10" inputmode="numeric" class="w-full border rounded-lg p-2" />
      </div>
      <div>
        <label class="block mb-1 text-sm font-medium">Gradimento</label>
        <select v-model="form.liked" class="w-full border rounded-lg p-2">
          <option :value="null">-</option>
          <option v-for="l in likedOptions" :key="l.value" :value="l.value">{{ l.label }}</option>
        </select>
      </div>
    </div>

    <!-- Dettagli TMDb -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
      <div>
        <label class="block mb-1 text-sm font-medium">Anno</label>
        <input v-model.number="form.release_year" type="number" class="w-full border rounded-lg p-2" placeholder="Es. 2010" />
      </div>
      <div>
        <label class="block mb-1 text-sm font-medium">Data di uscita</label>
        <input v-model.trim="form.release_date" type="text" class="w-full border rounded-lg p-2" placeholder="YYYY-MM-DD" />
      </div>
      <div>
        <label class="block mb-1 text-sm font-medium">Durata (min.)</label>
        <input v-model.number="form.runtime" type="number" min="1" class="w-full border rounded-lg p-2" placeholder="Es. 148" />
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
      <div>
        <label class="block mb-1 text-sm font-medium">Regista</label>
        <input v-model.trim="form.director" type="text" class="w-full border rounded-lg p-2" />
      </div>
      <div>
        <label class="block mb-1 text-sm font-medium">Cast (separa con virgole)</label>
        <input v-model.trim="castInput" type="text" class="w-full border rounded-lg p-2" placeholder="Nome 1, Nome 2, ..." />
      </div>
    </div>

    <!-- Trama (overview) -->
    <div>
      <label class="block mb-1 text-sm font-medium">Trama (da TMDb, opzionale)</label>
      <textarea
        v-model.trim="form.overview"
        rows="4"
        class="w-full border rounded-lg p-2 resize-y"
        placeholder="Descrizione del film in italiano"
      />
    </div>

    <!-- Nota -->
    <div>
      <label class="block mb-1 text-sm font-medium">Nota</label>
      <textarea v-model.trim="form.note" rows="3" class="w-full border rounded-lg p-2 resize-y" />
    </div>

    <!-- Azioni -->
    <div class="flex items-center justify-end gap-2">
      <button type="button" class="px-4 py-2 rounded border" @click="reset" :disabled="loading">
        Reset
      </button>
      <button
        type="submit"
        class="text-white bg-blue-700 hover:bg-blue-800 rounded px-4 py-2"
        :disabled="loading || !form.title"
      >
        <span v-if="!loading">Salva</span>
        <span v-else>Salvataggio…</span>
      </button>
    </div>
  </form>
</template>

<script setup>
const emit = defineEmits(['added'])
const { apiFetch } = useApi()

const props = defineProps({
  initialTitle: { type: String, default: '' },
  initialData: { type: Object, default: () => ({}) } // titolo/poster/overview ecc.
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

const form = reactive({
kind: 'movie',   // 👈 nuovo
  title: '',
  status: 'to_watch',
  score: null,
  liked: null,
  note: '',
  overview: '',            // 👈 campo overview

  // nuovi campi
  release_year: null,
  release_date: '',
  poster_url: '',
  director: '',
  cast: [],
  runtime: null,
  tmdb_id: null
})

const castInput = computed({
  get: () => (form.cast || []).join(', '),
  set: (v) => { form.cast = v ? v.split(',').map(s => s.trim()).filter(Boolean) : [] }
})

const loading = ref(false)

// Prefill iniziale (titolo + dati TMDb inclusa overview)
watch(() => props.initialTitle, (v) => { if (v) form.title = v }, { immediate: true })
watch(() => props.initialData, (d) => {
  if (!d) return
  if (d.kind)        form.kind = d.kind || form.kind              // 👈 prefill kind
  if (d.title)        form.title = d.title
  if (d.overview)     form.overview = d.overview          // 👈 prefill overview
  if (d.release_year !== undefined) form.release_year = d.release_year
  if (d.release_date !== undefined) form.release_date = d.release_date
  if (d.poster_url !== undefined)   form.poster_url = d.poster_url
  if (d.director !== undefined)     form.director = d.director
  if (Array.isArray(d.cast))        form.cast = d.cast
  if (d.runtime !== undefined)      form.runtime = d.runtime
  if (d.tmdb_id !== undefined)      form.tmdb_id = d.tmdb_id
}, { immediate: true })

function reset () {
   form.kind = 'movie'
  form.title = ''
  form.status = 'to_watch'
  form.score = null
  form.liked = null
  form.note = ''
  form.overview = ''               // 👈 reset overview

  form.release_year = null
  form.release_date = ''
  form.poster_url = ''
  form.director = ''
  form.cast = []
  form.runtime = null
  form.tmdb_id = null
}

async function submit () {
  loading.value = true
  try {
    const created = await apiFetch('/movies/', {
      method: 'POST',
      body: {
         kind: form.kind,               // 👈 nuovo
        title: form.title,
        status: form.status,
        score: form.score ?? null,
        liked: form.liked ?? null,
        note: form.note || null,
        overview: form.overview || null,               // 👈 INVIA overview

        release_year: form.release_year ?? null,
        release_date: form.release_date || null,
        poster_url: form.poster_url || null,
        director: form.director || null,
        cast: form.cast?.length ? form.cast : null,
        runtime: form.runtime ?? null,
        tmdb_id: form.tmdb_id ?? null
      }
    })
    reset()
    emit('added', created)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}
</script>
