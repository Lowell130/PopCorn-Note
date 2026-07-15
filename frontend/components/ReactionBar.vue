<template>
  <div class="flex items-center gap-2 flex-wrap select-none">
    <button
      v-for="reaction in reactionTypes"
      :key="reaction.type"
      @click="toggleReaction(reaction.type)"
      :class="[
        'flex items-center gap-1.5 bg-transparent border-0 outline-none transition-all duration-150 cursor-pointer p-0.5',
        hasUserReacted(reaction.type) 
          ? 'scale-125 opacity-100 filter drop-shadow-[0_0_6px_rgba(168,85,247,0.7)]' 
          : 'opacity-50 hover:opacity-100 hover:scale-110'
      ]"
      :title="reaction.label"
    >
      <span class="text-lg select-none">{{ reaction.emoji }}</span>
      <span 
        v-if="getCount(reaction.type) > 0" 
        class="text-xs font-bold"
        :class="hasUserReacted(reaction.type) ? 'text-purple-400' : 'text-gray-400'"
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
