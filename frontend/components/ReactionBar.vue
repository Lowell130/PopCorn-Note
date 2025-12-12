<template>
  <div class="flex items-center gap-1 flex-wrap mt-3 pt-3 border-t border-gray-100 dark:border-gray-700">
    <button
      v-for="reaction in reactionTypes"
      :key="reaction.type"
      @click="toggleReaction(reaction.type)"
      :class="[
        'flex items-center gap-1 px-2 py-1 rounded-full text-sm transition-all',
        hasUserReacted(reaction.type) 
          ? 'bg-blue-100 dark:bg-blue-900/30 ring-2 ring-blue-500' 
          : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
      ]"
      :title="reaction.label"
    >
      <span class="text-base">{{ reaction.emoji }}</span>
      <span 
        v-if="getCount(reaction.type) > 0" 
        class="text-xs font-medium"
        :class="hasUserReacted(reaction.type) ? 'text-blue-600 dark:text-blue-400' : 'text-gray-600 dark:text-gray-300'"
      >
        {{ getCount(reaction.type) }}
      </span>
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  activityId: { type: String, required: true },
  reactions: { type: Array, default: () => [] }
})

const emit = defineEmits(['updated'])
const { apiFetch } = useApi()
const { user } = useAuth()

const reactionTypes = [
  { type: 'like', emoji: '👍', label: 'Mi piace' },
  { type: 'love', emoji: '❤️', label: 'Lo adoro' },
  { type: 'funny', emoji: '😂', label: 'Divertente' },
  { type: 'fire', emoji: '🔥', label: 'Fantastico' },
  { type: 'popcorn', emoji: '🍿', label: 'Lo voglio vedere' },
  { type: 'dislike', emoji: '👎', label: 'Non mi piace' }
]

function getCount(type) {
  return props.reactions.filter(r => r.type === type).length
}

function hasUserReacted(type) {
  if (!user.value) return false
  const userId = user.value.id || user.value._id
  return props.reactions.some(r => r.type === type && r.user_id === userId)
}

function getUserReactionType() {
  if (!user.value) return null
  const userId = user.value.id || user.value._id
  const userReaction = props.reactions.find(r => r.user_id === userId)
  return userReaction?.type || null
}

async function toggleReaction(type) {
  const currentReaction = getUserReactionType()
  
  try {
    if (currentReaction === type) {
      // Rimuovi reazione
      await apiFetch(`/social/${props.activityId}/react`, { method: 'DELETE' })
    } else {
      // Aggiungi/cambia reazione
      await apiFetch(`/social/${props.activityId}/react`, {
        method: 'POST',
        body: { reaction_type: type }
      })
    }
    
    // Notifica il parent per aggiornare i dati
    emit('updated')
  } catch (e) {
    console.error('Reaction error', e)
  }
}
</script>
