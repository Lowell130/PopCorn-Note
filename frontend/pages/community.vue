<template>
  <div class="max-w-6xl mx-auto py-6 px-4">
    
    <!-- Title Block & Refresh -->
    <div class="flex items-center justify-between mb-8 animate-fade-in">
        <div>
            <h2 class="text-sm font-semibold text-purple-400 uppercase tracking-wider mb-1">
               Social
            </h2>
            <h1 class="text-4xl font-extrabold text-white tracking-tight">
               Community
            </h1>
            <p class="text-gray-400 mt-2">Cosa stanno guardando gli altri utenti?</p>
        </div>
        
        <!-- Refresh Button -->
        <button 
            @click="refreshAll"
            class="p-2.5 text-gray-400 hover:text-white hover:bg-white/10 rounded-xl transition cursor-pointer border border-white/5 bg-white/5"
            title="Aggiorna feed e classifica"
        >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
        </button>
    </div>

    <!-- Guide Banner (Explain Community) -->
    <div class="bg-purple-950/20 border border-purple-500/30 p-6 rounded-2xl flex items-start gap-4 shadow-xl backdrop-blur-md mb-8 animate-fade-in">
      <div class="p-3 bg-purple-500/10 border border-purple-500/20 rounded-xl text-purple-300 flex-shrink-0 select-none">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      </div>
      <div class="space-y-1 text-left">
        <h4 class="text-sm font-bold text-white">Il social hub di PopCorn-Note</h4>
        <p class="text-xs text-gray-300 leading-relaxed">
          La Community raccoglie le attività in tempo reale di tutti gli utenti registrati: scopri subito quando qualcuno aggiunge un nuovo titolo in lista o assegna una valutazione. 
          Puoi scrivere post personalizzati, inserire commenti sotto le schede attività degli altri membri e lasciare una reazione per condividere la tua passione per il cinema!
        </p>
      </div>
    </div>

    <!-- 2-Column Responsive Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      
      <!-- Left Column: Compose & Activities -->
      <div class="col-span-1 lg:col-span-8 space-y-6">
        <!-- Compose Box -->
        <div class="bg-white/5 border border-white/10 p-4 rounded-2xl shadow-xl animate-fade-in">
            <textarea
                v-model="newPostContent"
                rows="2"
                class="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 mb-3 resize-none transition"
                placeholder="Scrivi qualcosa alla community..."
            ></textarea>
            <div class="flex justify-end">
                 <button
                    @click="publishPost"
                    :disabled="!newPostContent.trim() || publishing"
                    class="px-5 py-2.5 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/40 text-purple-300 text-sm font-bold rounded-xl disabled:opacity-40 disabled:cursor-not-allowed transition flex items-center gap-2 hover:scale-102 duration-150 shadow-md cursor-pointer"
                 >
                    <span v-if="publishing" class="animate-spin">⌛</span>
                    <span>Pubblica</span>
                 </button>
            </div>
        </div>

        <!-- Feed List -->
        <div v-if="loading" class="space-y-4">
            <div v-for="n in 3" :key="n" class="bg-white/5 border border-white/5 h-24 rounded-2xl animate-pulse"></div>
        </div>

        <div v-else class="space-y-4">
            <FeedItem 
                v-for="item in feed" 
                :key="item.id" 
                :item="item" 
                @deleted="onDeleted"
                @reaction-updated="onReactionUpdated"
            />

            <!-- Spinner caricamento altro feed -->
            <div v-if="loadingMore" class="py-6 text-center">
              <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-purple-500 mx-auto"></div>
              <p class="text-xs text-gray-500 mt-2 font-semibold uppercase tracking-wider">Caricamento altre attività...</p>
            </div>

            <!-- Fine feed banner -->
            <div v-if="!hasMore && feed.length > 0" class="py-8 text-center text-gray-500 text-sm font-semibold select-none border-t border-white/5 mt-4">
              Hai raggiunto la fine del feed! 🎉
            </div>
            
            <div v-if="feed.length === 0" class="text-center py-12 text-gray-400">
                <div class="text-4xl mb-2">🦗</div>
                Nessuna attività recente. <br/>Sii il primo a scrivere qualcosa!
            </div>
        </div>
      </div>

      <!-- Right Column: Sidebar (Leaderboard & Quick Stats) -->
      <div class="col-span-1 lg:col-span-4 space-y-6">
        
        <!-- Active Members Sidebar -->
        <div class="bg-white/5 border border-white/10 rounded-3xl p-6 backdrop-blur-md text-left">
          <h3 class="text-lg font-bold text-white mb-4 flex items-center gap-2.5 border-b border-white/5 pb-3 select-none">
            <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
            </svg>
            Top Watchers
          </h3>
          
          <div v-if="loadingLeaderboard" class="space-y-3">
            <div v-for="n in 4" :key="n" class="h-10 bg-white/5 rounded-xl animate-pulse"></div>
          </div>
          
          <div v-else class="space-y-2.5">
            <div 
              v-for="(u, index) in leaderboard" 
              :key="u.id" 
              class="flex items-center justify-between p-2 hover:bg-white/5 rounded-xl transition-all duration-150"
            >
              <div class="flex items-center gap-3">
                <span class="text-xs font-bold text-gray-500 w-4 text-center">{{ index + 1 }}</span>
                <div 
                  class="w-8 h-8 rounded-full flex items-center justify-center text-white font-black text-xs shadow-md select-none"
                  :style="{ background: getAvatarColor(u.username) }"
                >
                  {{ u.username[0].toUpperCase() }}
                </div>
                <div class="flex flex-col">
                  <span class="text-sm font-semibold text-gray-200 line-clamp-1 flex items-center gap-1">
                    {{ u.username }}
                    <span v-if="u.is_admin" class="text-[9px] bg-purple-500/20 text-purple-300 px-1 py-0.5 rounded border border-purple-500/30 font-bold select-none">
                      Staff
                    </span>
                  </span>
                </div>
              </div>
              <span class="text-xs font-bold text-purple-400 select-none">
                🎬 {{ u.movies_count }}
              </span>
            </div>
            
            <div v-if="leaderboard.length === 0" class="text-sm text-gray-500 text-center py-4">
              Nessun utente registrato
            </div>
          </div>
        </div>

        <!-- Community Stats Card -->
        <div class="bg-white/5 border border-white/10 rounded-3xl p-6 backdrop-blur-md text-left">
          <h3 class="text-lg font-bold text-white mb-4 border-b border-white/5 pb-3 select-none">Statistiche Community</h3>
          <div class="space-y-3 text-sm">
            <div class="flex justify-between border-b border-white/5 pb-2">
              <span class="text-gray-400">Membri Totali</span>
              <span class="font-bold text-white">{{ leaderboard.length }}</span>
            </div>
            <div class="flex justify-between border-b border-white/5 pb-2">
              <span class="text-gray-400">Attività nel Feed</span>
              <span class="font-bold text-white">{{ feed.length }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">Stato server</span>
              <span class="font-semibold text-green-400 flex items-center gap-1 select-none">
                <span class="w-2 h-2 rounded-full bg-green-500 animate-ping inline-block"></span>
                Online
              </span>
            </div>
          </div>
        </div>

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

const leaderboard = ref([])
const loadingLeaderboard = ref(true)

// Paginazione Infinite Scroll
const limit = 20
const skip = ref(0)
const hasMore = ref(true)
const loadingMore = ref(false)

function onDeleted(id) {
    feed.value = feed.value.filter(i => i.id !== id)
    toast?.show?.('success', 'Post eliminato')
    loadLeaderboard() // Ricarica classifica
}

async function onReactionUpdated(activityId) {
    try {
        // Recupera abbastanza elementi per coprire quelli caricati in locale
        const allFeed = await apiFetch('/social/feed', {
            query: { limit: Math.max(100, feed.value.length) }
        })
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
    skip.value = 0
    hasMore.value = true
    try {
        const res = await apiFetch('/social/feed', {
            query: { limit, skip: skip.value }
        })
        feed.value = res.map(i => ({...i, id: i.id || i._id}))
        if (res.length < limit) {
            hasMore.value = false
        }
    } catch (e) {
        console.error("Feed error", e)
    } finally {
        loading.value = false
    }
}

async function loadMoreFeed() {
    if (loadingMore.value || !hasMore.value) return
    loadingMore.value = true
    try {
        const nextSkip = skip.value + limit
        const res = await apiFetch('/social/feed', {
            query: { limit, skip: nextSkip }
        })
        const mapped = res.map(i => ({...i, id: i.id || i._id}))
        
        // Evita duplicati nel feed
        const existingIds = new Set(feed.value.map(f => f.id))
        const uniqueNext = mapped.filter(item => !existingIds.has(item.id))
        
        feed.value.push(...uniqueNext)
        skip.value = nextSkip
        
        if (res.length < limit) {
            hasMore.value = false
        }
    } catch (e) {
        console.error("Load more feed error", e)
    } finally {
        loadingMore.value = false
    }
}

function handleScroll() {
  const scrollPosition = window.innerHeight + window.scrollY
  const threshold = document.documentElement.scrollHeight - 200
  if (scrollPosition >= threshold) {
    loadMoreFeed()
  }
}

async function loadLeaderboard() {
  loadingLeaderboard.value = true
  try {
    leaderboard.value = await apiFetch('/social/leaderboard')
  } catch (e) {
    console.error("Leaderboard error", e)
  } finally {
    loadingLeaderboard.value = false
  }
}

function refreshAll() {
  loadFeed()
  loadLeaderboard()
}

async function publishPost() {
    if (!newPostContent.value.trim()) return
    
    publishing.value = true
    try {
        const post = await apiFetch('/social/post', {
            method: 'POST',
            body: { content: newPostContent.value }
        })
        
        feed.value.unshift(post)
        newPostContent.value = ''
        toast?.show?.('success', 'Post pubblicato!')
        loadLeaderboard() // Ricarica classifica
    } catch (e) {
        toast?.show?.('error', 'Errore pubblicazione')
    } finally {
        publishing.value = false
    }
}

function getAvatarColor(name) {
    const strName = name || 'User'
    let hash = 0
    for (let i = 0; i < strName.length; i++) {
        hash = strName.charCodeAt(i) + ((hash << 5) - hash)
    }
    const h = Math.abs(hash % 360)
    return `linear-gradient(135deg, hsl(${h}, 70%, 60%), hsl(${h + 40}, 80%, 50%))`
}

onMounted(() => {
    loadFeed()
    loadLeaderboard()
    window.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
    window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.animate-fade-in { animation: fadeIn 0.5s ease-out; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>
