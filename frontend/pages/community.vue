<template>
  <div class="max-w-4xl mx-auto py-4 md:py-8 px-4 md:px-0">
    
    <div class="flex items-center justify-between mb-8 animate-fade-in">
        <div>
            <h1 class="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 mb-1">
                Community
            </h1>
            <p class="text-gray-500 dark:text-gray-400 text-sm">Cosa stanno guardando gli altri?</p>
        </div>
        
        <!-- Refresh Button -->
        <button 
            @click="loadFeed"
            class="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-full transition"
            title="Aggiorna feed"
        >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
        </button>
    </div>

    <!-- Compose Box -->
    <div class="bg-white dark:bg-gray-800 p-3 md:p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 mb-8 animate-fade-in">
        <textarea
            v-model="newPostContent"
            rows="2"
            class="w-full bg-gray-50 dark:bg-gray-700/50 border-0 rounded-lg p-3 text-sm focus:ring-2 focus:ring-blue-500 mb-3 resize-none dark:text-white"
            placeholder="Scrivi qualcosa alla community..."
        ></textarea>
        <div class="flex justify-end">
             <button
                @click="publishPost"
                :disabled="!newPostContent.trim() || publishing"
                class="px-5 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center gap-2"
             >
                <span v-if="publishing" class="animate-spin">⌛</span>
                <span>Pubblica</span>
             </button>
        </div>
    </div>

    <!-- Feed List -->
    <div v-if="loading" class="space-y-4">
        <!-- Scheletri semplici -->
        <div v-for="n in 3" :key="n" class="bg-gray-100 dark:bg-gray-800 h-24 rounded-xl animate-pulse"></div>
    </div>

    <div v-else class="space-y-4">
        <FeedItem 
            v-for="item in feed" 
            :key="item.id" 
            :item="item" 
            @deleted="onDeleted"
            @reaction-updated="onReactionUpdated"
        />
        
        <div v-if="feed.length === 0" class="text-center py-12 text-gray-400">
            <div class="text-4xl mb-2">🦗</div>
            Nessuna attività recente. <br/>Sii il primo a scrivere qualcosa!
        </div>
    </div>

  </div>
</template>

<script setup>
import FeedItem from '@/components/FeedItem.vue'

definePageMeta({ layout: 'wide' })
const { apiFetch } = useApi()
const toast = useToast?.()

const feed = ref([])
const loading = ref(true)
const publishing = ref(false)
const newPostContent = ref('')

function onDeleted(id) {
    feed.value = feed.value.filter(i => i.id !== id)
    toast?.show?.('success', 'Post eliminato')
}

async function onReactionUpdated(activityId) {
    // Ricarica solo l'item specifico
    try {
        const allFeed = await apiFetch('/social/feed')
        const updated = allFeed.find(item => item.id === activityId || item._id === activityId)
        if (updated) {
            const idx = feed.value.findIndex(i => i.id === activityId)
            if (idx !== -1) {
                feed.value[idx] = { ...updated, id: updated.id || updated._id }
            }
        }
    } catch (e) {
        console.error('Reaction update error', e)
    }
}

async function loadFeed() {
    loading.value = true
    try {
        const res = await apiFetch('/social/feed')
        feed.value = res.map(i => ({...i, id: i.id || i._id}))
    } catch (e) {
        console.error("Feed error", e)
    } finally {
        loading.value = false
    }
}

async function publishPost() {
    if (!newPostContent.value.trim()) return
    
    publishing.value = true
    try {
        const post = await apiFetch('/social/post', {
            method: 'POST',
            body: { content: newPostContent.value }
        })
        
        // Add to top
        feed.value.unshift(post)
        newPostContent.value = ''
        toast?.show?.('success', 'Post pubblicato!')
        
    } catch (e) {
        toast?.show?.('error', 'Errore pubblicazione')
    } finally {
        publishing.value = false
    }
}

onMounted(() => {
    loadFeed()
})
</script>

<style scoped>
.animate-fade-in { animation: fadeIn 0.5s ease-out; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>
