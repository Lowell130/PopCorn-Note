<template>
  <Transition
    enter-active-class="transition duration-200 ease-out"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="show"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4"
      @click.self="close"
    >
      <div class="bg-gray-900 border border-gray-700 rounded-xl w-full max-w-md shadow-2xl overflow-hidden">
        <!-- Header -->
        <div class="px-6 py-4 border-b border-gray-700 flex justify-between items-center bg-gray-800/50">
          <h3 class="text-lg font-bold text-white">Modifica: {{ item.title }}</h3>
          <button @click="close" class="text-gray-400 hover:text-white transition">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <!-- Body -->
        <div class="p-6 space-y-5">
          
          <!-- Stato -->
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Stato</label>
            <select
              v-model="draft.status"
              class="w-full bg-gray-800 border border-gray-600 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5"
            >
              <option v-for="s in statuses" :key="s.value" :value="s.value">
                {{ s.label }}
              </option>
            </select>
          </div>

          <!-- Score & Liked Row -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Voto (1-10)</label>
              <input
                v-model.number="draft.score"
                type="number"
                min="1"
                max="10"
                class="w-full bg-gray-800 border border-gray-600 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5"
              />
            </div>
            <div>
              <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Gradimento</label>
              <select
                v-model="draft.liked"
                class="w-full bg-gray-800 border border-gray-600 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5"
              >
                 <option :value="null">—</option>
                <option v-for="l in likedOptions" :key="l.value" :value="l.value">
                  {{ l.label }}
                </option>
              </select>
            </div>
          </div>

          <!-- Note -->
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Nota Personale</label>
            <textarea
              v-model="draft.note"
              rows="4"
              class="w-full bg-gray-800 border border-gray-600 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 resize-none"
              placeholder="Scrivi qui i tuoi pensieri..."
            ></textarea>
          </div>

        </div>

        <!-- Footer -->
        <div class="px-6 py-4 bg-gray-800/50 border-t border-gray-700 flex justify-between items-center">
            
            <button
            @click="remove"
            :disabled="loading"
            class="text-red-400 hover:text-red-300 hover:bg-red-900/30 text-sm font-medium px-4 py-2 rounded-lg transition border border-transparent hover:border-red-800"
          >
            Elimina dal DB
          </button>

          <div class="flex gap-3">
             <button
              @click="close"
              class="text-gray-300 hover:text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-white/10 transition"
            >
              Annulla
            </button>
            <button
              @click="save"
              :disabled="loading"
              class="bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium px-6 py-2 rounded-lg shadow-lg shadow-blue-900/30 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loading ? 'Salvataggio...' : 'Salva Modifiche' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
const props = defineProps({
  show: Boolean,
  item: { type: Object, required: true }
})

const emit = defineEmits(['close', 'updated', 'deleted'])

const { apiFetch } = useApi()
const toast = useToast()
const loading = ref(false)

const draft = reactive({
  status: 'to_watch',
  score: null,
  liked: null,
  note: ''
})

const statuses = [
  { value: "to_watch", label: "Da vedere" },
  { value: "watched", label: "Visto" },
  { value: "upcoming", label: "In uscita" },
  { value: "watching", label: "In visione" },
]

const likedOptions = [
  { value: "loved", label: "Mi è piaciuto molto" },
  { value: "liked", label: "Mi è piaciuto" },
  { value: "okay", label: "Carino" },
  { value: "disliked", label: "Non mi è piaciuto" },
  { value: "terrible", label: "Pessimo" },
]

// Sync draft on show
watch(() => props.show, (val) => {
  if (val && props.item) {
    draft.status = props.item.status || 'to_watch'
    draft.score = props.item.score
    draft.liked = props.item.liked
    draft.note = props.item.note
  }
})

function close() {
  emit('close')
}

async function save() {
  const score = (draft.score === "" || draft.score == null) 
    ? null 
    : Math.max(1, Math.min(10, Number(draft.score)))

  const body = {
    status: draft.status,
    score: score ?? undefined,
    liked: draft.liked ?? undefined,
    note: (draft.note ?? "").trim() || undefined,
  }

  loading.value = true
  try {
    const updated = await apiFetch(`/movies/${props.item.id}`, {
      method: 'PUT',
      body
    })
    emit('updated', updated)
    toast.show('success', 'Modifiche salvate!')
    close()
  } catch (e) {
    console.error(e)
    toast.show('error', 'Errore durante il salvataggio')
  } finally {
    loading.value = false
  }
}

async function remove() {
  if (!confirm(`Sei sicuro di voler eliminare "${props.item.title}"? Questa azione non può essere annullata.`)) return
  
  loading.value = true
  try {
    await apiFetch(`/movies/${props.item.id}`, { method: 'DELETE' })
    emit('deleted', props.item.id)
    toast.show('success', 'Elemento eliminato')
    close()
  } catch (e) {
    console.error(e)
    toast.show('error', 'Errore durante l\'eliminazione')
  } finally {
    loading.value = false
  }
}
</script>
