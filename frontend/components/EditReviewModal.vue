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
        <div class="p-6 space-y-5 overflow-y-auto max-h-[70vh] no-scrollbar">
          
          <!-- Stato (Segmented button group) -->
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-2.5">Stato</label>
            <div class="grid grid-cols-2 gap-2">
              <button
                v-for="s in statuses"
                :key="s.value"
                type="button"
                @click="draft.status = s.value"
                :class="[
                  'px-3 py-2.5 text-xs font-semibold rounded-xl border transition-all text-center flex items-center justify-center gap-1.5',
                  draft.status === s.value
                    ? getStatusColorClass(s.value)
                    : 'bg-gray-800 border-gray-700 text-gray-400 hover:bg-gray-750 hover:text-white'
                ]"
              >
                <span>{{ s.label }}</span>
              </button>
            </div>
          </div>

          <!-- Voto Personale (Interactive Progress Bar) -->
          <div class="space-y-2">
            <div class="flex justify-between items-center">
              <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest">Voto Personale</label>
              <span v-if="draft.score" class="text-xs font-bold text-blue-400 bg-blue-500/10 border border-blue-500/20 px-2.5 py-0.5 rounded-md">
                {{ draft.score }} / 10 {{ getScoreSentiment(draft.score) }}
              </span>
              <span v-else class="text-xs text-gray-500 italic">Nessun voto</span>
            </div>
            
            <!-- Interactive Track -->
            <div class="relative flex items-center h-9 bg-gray-800 border border-gray-700 rounded-xl overflow-hidden p-1 select-none">
              <!-- Clickable Zones -->
              <div
                v-for="i in 10"
                :key="i"
                @click="draft.score = i"
                class="flex-1 h-full cursor-pointer relative z-10"
              >
                <div class="absolute inset-y-0 right-0 w-px bg-gray-750"></div>
              </div>

              <!-- Dynamic Fill -->
              <div
                class="absolute inset-y-0 left-0 bg-gradient-to-r from-blue-600 to-indigo-500 transition-all duration-200 pointer-events-none"
                :style="{ width: draft.score ? `${draft.score * 10}%` : '0%' }"
              >
                <div class="absolute right-0 top-0 bottom-0 w-2 bg-white/30 blur-[2px]"></div>
              </div>
            </div>

            <!-- Labels 1-10 -->
            <div class="flex justify-between px-1 text-[10px] text-gray-500 font-semibold select-none">
              <span
                v-for="i in 10"
                :key="i"
                @click="draft.score = i"
                class="cursor-pointer hover:text-blue-400 transition"
                :class="{ 'text-blue-300 font-bold': draft.score === i }"
              >
                {{ i }}
              </span>
            </div>

            <div class="flex justify-end" v-if="draft.score != null">
              <button
                type="button"
                @click="draft.score = null"
                class="text-xs text-red-400 hover:text-red-300 transition"
              >
                Rimuovi voto
              </button>
            </div>
          </div>



          <!-- Tagging (Categories) -->
          <div class="space-y-2">
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest">Tag / Categorie</label>
            <div class="flex flex-wrap gap-1.5 p-2.5 bg-gray-800 border border-gray-700 rounded-xl focus-within:border-blue-500/50 focus-within:ring-1 focus-within:ring-blue-500/50 transition-all">
              <span
                v-for="(t, idx) in draft.tags"
                :key="idx"
                class="inline-flex items-center gap-1 px-2.5 py-0.5 bg-blue-500/10 border border-blue-500/20 text-blue-300 text-xs font-medium rounded-lg"
              >
                {{ t }}
                <button
                  type="button"
                  @click="removeTag(idx)"
                  class="text-blue-400 hover:text-blue-200 transition font-bold"
                >
                  &times;
                </button>
              </span>
              <input
                v-model="newTagInput"
                @keydown.enter.prevent="addTag"
                @keydown.comma.prevent="addTag"
                @blur="addTag"
                placeholder="Scrivi tag e premi Invio..."
                class="flex-1 min-w-[120px] bg-transparent border-0 text-white text-xs p-0.5 focus:ring-0 focus:outline-none placeholder-gray-600"
              />
            </div>
          </div>

          <!-- Nota -->
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">Nota Personale</label>
            <textarea
              v-model="draft.note"
              rows="4"
              class="w-full bg-gray-800 border border-gray-700 text-white text-sm rounded-xl p-3 focus:ring-blue-500 focus:border-blue-500 block resize-none outline-none placeholder-gray-600 transition-all"
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
  note: '',
  tags: []
})

const statuses = [
  { value: "to_watch", label: "Da vedere" },
  { value: "watched", label: "Visto" },
  { value: "upcoming", label: "In uscita" },
  { value: "watching", label: "In visione" },
]



const newTagInput = ref("")

function addTag() {
  const tag = newTagInput.value.trim().toLowerCase()
  if (tag && !draft.tags.includes(tag)) {
    draft.tags.push(tag)
  }
  newTagInput.value = ""
}

function removeTag(index) {
  draft.tags.splice(index, 1)
}

function getStatusColorClass(value) {
  switch (value) {
    case 'to_watch':
      return 'bg-amber-500/10 border-amber-500 text-amber-400 shadow-md shadow-amber-500/10';
    case 'watched':
      return 'bg-emerald-500/10 border-emerald-500 text-emerald-400 shadow-md shadow-emerald-500/10';
    case 'upcoming':
      return 'bg-cyan-500/10 border-cyan-500 text-cyan-400 shadow-md shadow-cyan-500/10';
    case 'watching':
      return 'bg-fuchsia-500/10 border-fuchsia-500 text-fuchsia-400 shadow-md shadow-fuchsia-500/10';
    default:
      return 'bg-blue-500/10 border-blue-500 text-blue-400 shadow-md shadow-blue-500/10';
  }
}

function getScoreSentiment(score) {
  if (!score) return "";
  if (score >= 9) return "❤️ Amo";
  if (score >= 7) return "👍 Piace";
  if (score >= 5) return "😐 Carino";
  if (score >= 3) return "👎 No";
  return "💩 Pessimo";
}

// Sync draft on show
watch(() => props.show, (val) => {
  if (val && props.item) {
    draft.status = props.item.status || 'to_watch'
    draft.score = props.item.score
    draft.liked = props.item.liked
    draft.note = props.item.note
    draft.tags = props.item.tags ? [...props.item.tags] : []
    newTagInput.value = ""
  }
})

function close() {
  emit('close')
}

async function save() {
  addTag()

  const score = (draft.score === "" || draft.score == null) 
    ? null 
    : Math.max(1, Math.min(10, Number(draft.score)))

  // Calcola il gradimento basato sul voto per rimuovere la ridondanza
  let liked = null
  if (score != null) {
    if (score >= 9) liked = "loved"
    else if (score >= 7) liked = "liked"
    else if (score >= 5) liked = "okay"
    else if (score >= 3) liked = "disliked"
    else liked = "terrible"
  }

  const body = {
    status: draft.status,
    score: score,
    liked: liked,
    note: (draft.note ?? "").trim() === "" ? null : (draft.note ?? "").trim(),
    tags: draft.tags || [],
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

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
