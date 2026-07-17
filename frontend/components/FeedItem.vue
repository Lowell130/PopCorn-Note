<template>
  <div class="bg-white/5 border border-white/10 rounded-2xl p-4 shadow-xl flex gap-3 md:gap-4 animate-fade-in-up text-white">
    
    <!-- Avatar -->
    <div class="flex-shrink-0">
      <div 
        class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm shadow-md transition-transform hover:scale-105"
        :style="{ background: avatarGivenColor }"
      >
        {{ (item.username || 'U')[0].toUpperCase() }}
      </div>
    </div>

    <!-- Content -->
    <div class="flex-1 min-w-0">
      <div class="flex items-center justify-between mb-1">
        <h4 class="text-sm font-bold text-white">
          {{ item.username }}
        </h4>
        <span class="text-xs text-gray-500">
           {{ formatDate(item.created_at) }}
        </span>
      </div>

      <!-- Text -->
      <p class="text-gray-300 text-sm leading-relaxed mb-3">
        <span v-if="item.type !== 'post'" class="text-purple-400 italic mr-1">
            {{ item.type === 'add_movie' ? '🎬' : '⭐' }}
        </span>
        {{ item.content }}
      </p>

      <!-- Movie Attachment (if any) -->
      <div 
        v-if="item.movie_title && item.movie_poster"
        class="flex gap-3 bg-white/5 p-3 rounded-xl border border-white/5 hover:border-white/10 hover:bg-white/10 transition cursor-pointer"
        @click="goToMovie(item.movie_id)"
      >
        <img :src="item.movie_poster" class="w-10 h-14 object-cover rounded shadow-sm bg-white/10" loading="lazy" />
        <div class="flex flex-col justify-center">
             <h5 class="text-sm font-semibold text-white line-clamp-1">
                 {{ item.movie_title }}
             </h5>
             <span v-if="item.movie_score" class="text-xs text-amber-400 font-semibold">
                 ⭐ {{ item.movie_score }}/10
             </span>
        </div>
      </div>

      <!-- Actions Bar -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mt-3 pt-3 border-t border-white/5">
          <ReactionBar 
            :activity-id="item.id" 
            :reactions="item.reactions || []"
            @updated="$emit('reaction-updated', item.id)"
          />
          
          <!-- Comment Toggle -->
          <button 
            @click="toggleComments"
            class="flex items-center justify-center sm:justify-start gap-1.5 text-xs font-semibold text-gray-300 hover:text-white transition px-3 py-2 sm:py-1.5 w-full sm:w-auto rounded-full bg-white/5 hover:bg-white/10 border border-white/5"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
            <span>{{ comments.length ? comments.length : 'Commenta' }}</span>
          </button>
      </div>

      <!-- Comments Section -->
      <div v-if="showComments" class="mt-3 space-y-3 pl-2 md:pl-4 border-l-2 border-white/10 animate-fade-in-up">
          <!-- Existing Comments -->
          <div v-for="c in comments" :key="c.id" class="group/comment flex gap-2 text-sm items-start">
              <div class="font-bold text-purple-400 text-xs whitespace-nowrap">{{ c.username }}:</div>
              <div class="text-gray-300 flex-1 break-words">{{ c.content }}</div>
              
              <!-- Delete Comment Button (Admin or Author) -->
              <button 
                 v-if="isAdmin || user?.id === c.user_id"
                 @click="deleteComment(c.id)"
                 class="opacity-0 group-hover/comment:opacity-100 text-gray-500 hover:text-red-400 transition px-1 cursor-pointer"
                 title="Elimina commento"
              >
                 <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
              </button>
          </div>

          <!-- Add Comment -->
          <div class="flex gap-2">
              <input 
                 v-model="newComment"
                 type="text" 
                 placeholder="Scrivi un commento..." 
                 class="flex-1 bg-white/5 border border-white/10 text-white placeholder-gray-500 rounded-xl px-3 py-1.5 text-sm focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition"
                 @keyup.enter="postComment"
              />
              <button 
                 @click="postComment"
                 :disabled="!newComment.trim() || submitting"
                 class="text-purple-400 hover:text-purple-300 disabled:opacity-50 text-sm font-semibold px-2 cursor-pointer"
              >
                 Invia
              </button>
          </div>
      </div>

    </div>

    <!-- Delete Action (Admin) -->
    <button 
        v-if="isAdmin" 
        @click="deleteItem"
        class="text-gray-400 hover:text-red-500 transition self-start p-1 cursor-pointer"
        title="Elimina (Admin)"
    >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
    </button>

  </div>
</template>

<script setup>
import ReactionBar from '@/components/ReactionBar.vue'

const props = defineProps({
  item: { type: Object, required: true }
})
const emit = defineEmits(['deleted', 'reaction-updated'])
const router = useRouter()
const { isAdmin, user } = useAuth()
const { apiFetch } = useApi()

const showComments = ref(false)
const newComment = ref('')
const submitting = ref(false)
const localComments = ref([])

onMounted(() => {
    // Inizializza commenti se presenti nell'item (il backend li deve tornare)
    // Se il backend non popola ancora i commenti nel feed principale, si potrebbero caricare on demand
    // Per ora assumiamo che item.comments esista o lo inizializziamo vuoto
    if (props.item.comments) {
        localComments.value = [...props.item.comments]
    }
})

const comments = computed(() => localComments.value)

// Dynamic Avatar Color
const avatarGivenColor = computed(() => {
    const name = props.item.username || 'User'
    let hash = 0
    for (let i = 0; i < name.length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash)
    }
    const h = Math.abs(hash % 360)
    return `linear-gradient(135deg, hsl(${h}, 70%, 60%), hsl(${h + 40}, 80%, 50%))`
})

function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit' })
}

function goToMovie(id) {
    if(id) {
       navigateTo(`/movies/${id}`)
    }
}

async function deleteItem() {
    if (!confirm('Eliminare questa attività?')) return
    try {
        await apiFetch(`/social/${props.item.id}`, { method: 'DELETE' })
        emit('deleted', props.item.id)
    } catch (e) {
        console.error(e)
        alert('Errore eliminazione')
    }
}

function toggleComments() {
    showComments.value = !showComments.value
}

async function postComment() {
    if (!newComment.value.trim()) return
    submitting.value = true
    try {
        const added = await apiFetch(`/social/${props.item.id}/comments`, {
            method: 'POST',
            body: { content: newComment.value }
        })
        localComments.value.push(added)
        newComment.value = ''
    } catch (e) {
        console.error(e)
    } finally {
        submitting.value = false
    }
}

async function deleteComment(commentId) {
    if (!confirm('Eliminare questo commento?')) return
    try {
        await apiFetch(`/social/${props.item.id}/comments/${commentId}`, { method: 'DELETE' })
        localComments.value = localComments.value.filter(c => c.id !== commentId)
    } catch (e) {
        console.error(e)
    }
}
</script>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.5s ease-out forwards;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
