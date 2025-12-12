<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-5 flex gap-4 animate-fade-in-up">
    
    <!-- Avatar -->
    <div class="flex-shrink-0">
      <div 
        class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm bg-gradient-to-br from-blue-500 to-indigo-600 shadow-md"
      >
        {{ (item.username || 'U')[0].toUpperCase() }}
      </div>
    </div>

    <!-- Content -->
    <div class="flex-1 min-w-0">
      <div class="flex items-center justify-between mb-1">
        <h4 class="text-sm font-bold text-gray-900 dark:text-white">
          {{ item.username }}
        </h4>
        <span class="text-xs text-gray-400">
           {{ formatDate(item.created_at) }}
        </span>
      </div>

      <!-- Text -->
      <p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed mb-3">
        <span v-if="item.type !== 'post'" class="text-gray-400 italic mr-1">
            {{ item.type === 'add_movie' ? '🎬' : '⭐' }}
        </span>
        {{ item.content }}
      </p>

      <!-- Movie Attachment (if any) -->
      <div 
        v-if="item.movie_title && item.movie_poster"
        class="flex gap-3 bg-gray-50 dark:bg-gray-700/50 p-3 rounded-lg border border-gray-100 dark:border-gray-700/50 transition hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer"
        @click="goToMovie(item.movie_id)"
      >
        <img :src="item.movie_poster" class="w-10 h-14 object-cover rounded shadow-sm bg-gray-200" loading="lazy" />
        <div class="flex flex-col justify-center">
             <h5 class="text-sm font-semibold text-gray-800 dark:text-gray-200 line-clamp-1">
                 {{ item.movie_title }}
             </h5>
             <span v-if="item.movie_score" class="text-xs text-amber-500 font-medium">
                 ⭐ {{ item.movie_score }}/10
             </span>
        </div>
      </div>

      <!-- Reactions -->
      <ReactionBar 
        :activity-id="item.id" 
        :reactions="item.reactions || []"
        @updated="$emit('reaction-updated', item.id)"
      />
    </div>

    <!-- Delete Action (Admin) -->
    <button 
        v-if="isAdmin" 
        @click="deleteItem"
        class="text-gray-400 hover:text-red-600 transition self-start p-1"
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
const { isAdmin } = useAuth()
const { apiFetch } = useApi()

function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit' })
}

function goToMovie(id) {
    if(id) {
        // Al momento non abbiamo una pagina dettaglio pubblica, ma potremmo averla
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
