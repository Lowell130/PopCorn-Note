<!-- components/PopcornBot.vue -->
<template>
  <div v-if="isLoggedIn && usageInfo.ai_bot_enabled">
    <!-- Floating Toggle Button -->
    <button
      @click="toggleChat"
      class="fixed bottom-20 right-6 z-50 p-4 bg-gradient-to-r from-purple-600 via-pink-600 to-amber-500 hover:from-purple-500 hover:to-amber-400 bg-no-repeat text-white rounded-full shadow-2xl shadow-purple-600/40 transform hover:scale-105 active:scale-95 transition-all duration-300 flex items-center gap-2 group border border-white/20"
      aria-label="Apri PopCorn Bot AI"
    >
      <span class="text-2xl group-hover:rotate-12 transition-transform duration-300">🍿</span>
      <span class="font-bold text-sm hidden sm:inline tracking-wide">PopCorn Bot</span>
      <!-- Badge notifiche/status -->
      <span class="relative flex h-3 w-3">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-3 w-3 bg-amber-500"></span>
      </span>
    </button>

    <!-- Chat Drawer Window -->
    <div
      v-if="isOpen"
      class="fixed bottom-[152px] right-4 sm:right-6 z-50 w-[calc(100vw-2rem)] sm:w-[420px] max-h-[620px] h-[calc(100vh-10rem)] gradient-border rounded-3xl shadow-2xl backdrop-blur-2xl flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-5 duration-300"
    >
      <!-- Header -->
      <div class="px-5 py-4 border-b border-white/10 bg-slate-900/80 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-purple-600 to-amber-500 flex items-center justify-center text-xl shadow-md">
            🍿
          </div>
          <div>
            <h3 class="font-bold text-white text-base tracking-tight flex items-center gap-2">
              <span>PopCorn Bot</span>
              <span class="text-[10px] uppercase tracking-wider font-extrabold px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30">AI</span>
            </h3>
            <p class="text-xs text-gray-400 flex items-center gap-1.5 mt-0.5">
              <span v-if="usageInfo.is_admin" class="text-amber-400 font-semibold">👑 Admin (Richieste Illimitate)</span>
              <span v-else-if="usageInfo.remaining === 0" class="text-rose-400">⚠️ Limite giornaliero raggiunto (0/1)</span>
              <span v-else class="text-emerald-400">Richieste oggi: {{ usageInfo.today_count }}/{{ usageInfo.daily_limit }}</span>
            </p>
          </div>
        </div>

        <button
          @click="isOpen = false"
          class="w-8 h-8 rounded-full bg-white/5 hover:bg-white/10 text-gray-400 hover:text-white flex items-center justify-center transition-colors text-sm"
        >
          ✕
        </button>
      </div>

      <!-- Chat Messages Container -->
      <div ref="messagesContainer" class="flex-1 overflow-y-auto overflow-x-hidden p-4 space-y-4 no-scrollbar">
        <!-- Welcome Message -->
        <div class="flex items-start gap-3">
          <div class="w-8 h-8 rounded-xl bg-purple-600/30 border border-purple-500/30 flex items-center justify-center text-base shrink-0">
            🍿
          </div>
          <div class="bg-slate-900/80 border border-white/10 text-gray-200 text-sm rounded-2xl rounded-tl-none p-4 max-w-[88%] space-y-2 break-words [overflow-wrap:anywhere]">
            <p class="font-medium text-white">Ciao! Sono PopCorn Bot 🍿</p>
            <p class="text-xs text-gray-300 leading-relaxed">
              Il tuo assistente cinefilo personale. Dimmi cosa hai voglia di vedere stasera o chiedimi consigli basati sulla tua libreria!
            </p>

            <!-- Quick Prompts Chips -->
            <div class="pt-2 flex flex-wrap gap-1.5">
              <button
                v-for="(prompt, idx) in quickPrompts"
                :key="idx"
                @click="sendQuickPrompt(prompt)"
                :disabled="cannotRequest"
                class="text-xs bg-purple-500/10 hover:bg-purple-500/20 border border-purple-500/30 text-purple-300 px-2.5 py-1 rounded-lg transition-all text-left disabled:opacity-50"
              >
                ✨ {{ prompt }}
              </button>
            </div>
          </div>
        </div>

        <!-- History Messages -->
        <div v-for="(msg, index) in messages" :key="index" class="space-y-3">
          <!-- User message -->
          <div v-if="msg.role === 'user'" class="flex justify-end">
            <div class="bg-gradient-to-r from-purple-600 to-indigo-600 text-white text-sm rounded-2xl rounded-tr-none px-4 py-3 max-w-[85%] shadow-md break-words [overflow-wrap:anywhere]">
              {{ msg.content }}
            </div>
          </div>

          <!-- Bot message -->
          <div v-else class="flex items-start gap-3">
            <div class="w-8 h-8 rounded-xl bg-purple-600/30 border border-purple-500/30 flex items-center justify-center text-base shrink-0">
              🍿
            </div>
            <div class="bg-slate-900/80 border border-white/10 text-gray-200 text-sm rounded-2xl rounded-tl-none p-4 max-w-[88%] space-y-3 break-words [overflow-wrap:anywhere]">
              <!-- Text content -->
              <p class="whitespace-pre-line leading-relaxed text-xs sm:text-sm break-words [overflow-wrap:anywhere]">{{ msg.content }}</p>

              <!-- Movie Recommendation Cards -->
              <div v-if="msg.recommendations && msg.recommendations.length > 0" class="space-y-3 pt-2">
                <p class="text-xs font-bold text-amber-400 uppercase tracking-wider">🎯 Titoli Consigliati per te:</p>

                <div
                  v-for="(rec, rIdx) in msg.recommendations"
                  :key="rIdx"
                  class="bg-slate-950/80 border border-white/10 rounded-xl p-3 flex gap-3 items-center hover:border-purple-500/30 transition-all"
                >
                  <!-- Poster image -->
                  <img
                    v-if="rec.poster_path"
                    :src="getPosterUrl(rec.poster_path)"
                    :alt="rec.title"
                    class="w-14 h-20 object-cover rounded-lg shadow-md shrink-0 bg-slate-900 border border-white/10"
                  />
                  <div v-else class="w-14 h-20 bg-slate-900 rounded-lg flex items-center justify-center text-xl shrink-0 border border-white/5">
                    🎬
                  </div>

                  <!-- Info & Actions -->
                  <div class="flex-1 min-w-0 space-y-1">
                    <div class="flex items-center justify-between gap-1">
                      <h4 class="font-bold text-white text-xs truncate">{{ rec.title }}</h4>
                      <span v-if="rec.vote_average" class="text-[10px] font-bold text-amber-400 flex items-center gap-0.5 shrink-0">
                        ⭐ {{ Number(rec.vote_average).toFixed(1) }}
                      </span>
                    </div>

                    <p class="text-[11px] text-gray-400">
                      <span class="capitalize">{{ rec.kind === 'tv' ? 'Serie TV' : 'Film' }}</span>
                      <span v-if="rec.release_year"> • {{ rec.release_year }}</span>
                    </p>

                    <p v-if="rec.reason" class="text-[11px] text-purple-300/90 line-clamp-2 italic">
                      "{{ rec.reason }}"
                    </p>

                    <!-- Action Button -->
                    <div class="pt-1">
                      <button
                        v-if="rec.in_user_library || rec.added"
                        disabled
                        class="px-2.5 py-1 bg-emerald-500/20 text-emerald-300 text-[11px] font-semibold rounded-lg border border-emerald-500/30 flex items-center gap-1 cursor-default"
                      >
                        ✓ Nella tua Lista
                      </button>

                      <button
                        v-else
                        @click="addToCollection(rec)"
                        :disabled="rec.adding"
                        class="px-2.5 py-1 bg-purple-600 hover:bg-purple-500 text-white text-[11px] font-semibold rounded-lg transition-all shadow-md flex items-center gap-1 disabled:opacity-50"
                      >
                        <span v-if="rec.adding" class="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                        <span v-else>➕ Aggiungi alla tua Lista</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Typing Indicator -->
        <div v-if="isTyping" class="flex items-start gap-3">
          <div class="w-8 h-8 rounded-xl bg-purple-600/30 border border-purple-500/30 flex items-center justify-center text-base shrink-0">
            🍿
          </div>
          <div class="bg-slate-900/80 border border-white/10 rounded-2xl rounded-tl-none p-4 flex items-center gap-1.5">
            <span class="w-2 h-2 bg-purple-400 rounded-full animate-bounce"></span>
            <span class="w-2 h-2 bg-purple-400 rounded-full animate-bounce [animation-delay:0.2s]"></span>
            <span class="w-2 h-2 bg-purple-400 rounded-full animate-bounce [animation-delay:0.4s]"></span>
          </div>
        </div>
      </div>

      <!-- Limit Reached Alert -->
      <div v-if="cannotRequest" class="px-4 py-2 bg-rose-500/10 border-t border-rose-500/20 text-rose-300 text-xs text-center font-medium">
        🔒 Hai raggiunto il tuo limite di 1 richiesta al giorno. Torna domani!
      </div>

      <!-- Footer / Input Area -->
      <form @submit.prevent="sendMessage" class="p-3 bg-slate-900 border-t border-white/10 flex items-center gap-2">
        <input
          v-model="inputQuery"
          type="text"
          placeholder="Chiedi al Bot... (es. Consigliami un thriller)"
          :disabled="isTyping || cannotRequest"
          class="flex-1 bg-slate-950 border border-white/10 rounded-xl px-4 py-2.5 text-white text-xs sm:text-sm focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all disabled:opacity-50"
        />
        <button
          type="submit"
          :disabled="!inputQuery.trim() || isTyping || cannotRequest"
          class="px-4 py-2.5 bg-purple-600 hover:bg-purple-500 disabled:opacity-40 text-white rounded-xl font-bold text-xs transition-all shadow-md shrink-0 flex items-center gap-1"
        >
          <span>Invia</span>
          <span>➔</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'
import { useAuth } from '~/composables/useAuth'

const { apiFetch } = useApi()
const { isLoggedIn } = useAuth()

const isOpen = ref(false)
const inputQuery = ref('')
const isTyping = ref(false)
const messagesContainer = ref(null)

const messages = ref([])

const usageInfo = ref({
  is_admin: false,
  today_count: 0,
  daily_limit: 1,
  remaining: 1,
  can_request: true,
  ai_bot_enabled: true
})

const quickPrompts = [
  "Consigliami un film da max 90 min",
  "Thriller psicologico coinvolgente",
  "Film divertente per la serata",
  "Qualcosa di simile a Interstellar"
]

const cannotRequest = computed(() => {
  return !usageInfo.value.can_request && !usageInfo.value.is_admin
})

const getPosterUrl = (path) => {
  if (!path) return null
  if (path.startsWith('http')) return path
  const cleanPath = path.startsWith('/') ? path : `/${path}`
  return `https://image.tmdb.org/t/p/w500${cleanPath}`
}

const fetchUsage = async () => {
  if (!isLoggedIn.value) return
  try {
    const data = await apiFetch('/ai/usage')
    if (data) {
      usageInfo.value = {
        ...data,
        ai_bot_enabled: data.ai_bot_enabled !== false
      }
    }
  } catch (err) {
    // ignoriamo se non autenticato
  }
}

const toggleChat = async () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    await fetchUsage()
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const sendQuickPrompt = (promptText) => {
  inputQuery.value = promptText
  sendMessage()
}

const sendMessage = async () => {
  const query = inputQuery.value.trim()
  if (!query || isTyping.value || cannotRequest.value) return

  // Aggiungi messaggio utente alla chat
  messages.value.push({ role: 'user', content: query })
  inputQuery.value = ''
  isTyping.value = true
  await scrollToBottom()

  // Prepara lo storico per il backend
  const historyForBackend = messages.value.map(m => ({
    role: m.role,
    content: m.content
  }))

  try {
    const res = await apiFetch('/ai/chat', {
      method: 'POST',
      body: {
        message: query,
        chat_history: historyForBackend
      }
    })

    if (res) {
      messages.value.push({
        role: 'assistant',
        content: res.reply,
        recommendations: res.recommendations || []
      })
      if (res.usage) {
        usageInfo.value = {
          ...res.usage,
          ai_bot_enabled: res.usage.ai_bot_enabled !== false
        }
      }
    }
  } catch (err) {
    const errorDetail = err?.data?.detail || 'Si è verificato un errore durante la generazione dei consigli.'
    messages.value.push({
      role: 'assistant',
      content: `⚠️ ${errorDetail}`,
      recommendations: []
    })
  } finally {
    isTyping.value = false
    await scrollToBottom()
  }
}

const addToCollection = async (rec) => {
  rec.adding = true
  try {
    let details = null
    if (rec.tmdb_id) {
      const endpoint = rec.kind === 'tv' ? `/tmdb/tv/${rec.tmdb_id}` : `/tmdb/details/${rec.tmdb_id}`
      details = await apiFetch(endpoint).catch(() => null)
    }

    const body = {
      kind: rec.kind || 'movie',
      title: details?.title || rec.title,
      status: 'to_watch',
      release_date: details?.release_date || null,
      release_year: details?.release_year || (rec.release_year ? Number(rec.release_year) : null),
      poster_url: details?.poster_url || (rec.poster_path ? `https://image.tmdb.org/t/p/w500${rec.poster_path}` : null),
      director: details?.director || null,
      cast: Array.isArray(details?.cast) ? details.cast : null,
      runtime: details?.runtime || null,
      tmdb_id: rec.tmdb_id ? Number(rec.tmdb_id) : null,
      overview: details?.overview || rec.overview || null,
      tmdb_vote: details?.vote_average || rec.vote_average || null
    }

    const saved = await apiFetch('/movies/', {
      method: 'POST',
      body
    })

    rec.added = true
    rec.in_user_library = true
    rec.saved_id = saved.id
    if (import.meta.client) {
      document.dispatchEvent(new CustomEvent('collection-updated'))
    }
  } catch (err) {
    if (err?.response?.status === 409 || err?.status === 409) {
      rec.added = true
      rec.in_user_library = true
    } else {
      alert(err?.data?.detail || 'Impossibile aggiungere il titolo alla tua lista.')
    }
  } finally {
    rec.adding = false
  }
}

onMounted(() => {
  if (isLoggedIn.value) {
    fetchUsage()
  }
})
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none !important;
}
.no-scrollbar {
  -ms-overflow-style: none !important;
  scrollbar-width: none !important;
}
.gradient-border {
  border: 2px solid transparent;
  background: 
    linear-gradient(to bottom, rgba(2, 6, 23, 0.96), rgba(2, 6, 23, 0.96)) padding-box,
    linear-gradient(to right, #9333ea, #db2777, #f59e0b) border-box;
}
</style>

