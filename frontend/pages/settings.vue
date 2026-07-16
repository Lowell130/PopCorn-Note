<template>
  <div class="max-w-2xl mx-auto py-10 px-4 space-y-8 text-left">
    
    <!-- Title Block -->
    <div class="border-b border-white/10 pb-6 mb-8">
      <h2 class="text-sm font-semibold text-purple-400 uppercase tracking-wider mb-1">
         Pannello
      </h2>
      <h1 class="text-4xl font-extrabold text-white tracking-tight">
         Impostazioni
      </h1>
    </div>

    <!-- Profilo Card -->
    <div class="bg-white/5 border border-white/10 rounded-3xl p-6 backdrop-blur-md text-white shadow-xl">
      <h2 class="text-xl font-bold mb-4 text-white flex items-center gap-2">
        <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
        Il tuo Profilo
      </h2>
      
      <div v-if="user" class="space-y-4">
        <div class="border-b border-white/5 pb-3">
          <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Email</label>
          <div class="text-base font-semibold text-white">{{ user.email }}</div>
        </div>
        
        <div>
          <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Username</label>
          <div class="text-base font-semibold text-white">{{ user.username || '—' }}</div>
        </div>
      </div>
    </div>

    <!-- Esporta i tuoi Dati -->
    <div class="bg-white/5 border border-white/10 rounded-3xl p-6 backdrop-blur-md text-white shadow-xl">
      <h2 class="text-xl font-bold mb-2 text-white flex items-center gap-2">
        <svg class="w-5 h-5 text-sky-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        Esporta i tuoi Dati
      </h2>
      <p class="text-xs text-gray-400 mb-6 leading-relaxed">
        Scarica una copia locale completa di tutti i film e le serie TV che hai salvato nella tua Dashboard in formato standard JSON o CSV. 
        Potrai importarla in altri software o aprirla in Excel.
      </p>
      
      <div class="flex flex-wrap gap-3">
        <button
          @click="exportJSON"
          class="inline-flex items-center gap-2 px-5 py-2.5 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/40 text-purple-300 font-bold rounded-xl text-xs transition cursor-pointer shadow-md shadow-purple-500/5 hover:scale-102"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Esporta in JSON
        </button>

        <button
          @click="exportCSV"
          class="inline-flex items-center gap-2 px-5 py-2.5 bg-sky-500/20 hover:bg-sky-500/30 border border-sky-500/40 text-sky-300 font-bold rounded-xl text-xs transition cursor-pointer shadow-md shadow-sky-500/5 hover:scale-102"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Esporta in CSV
        </button>
      </div>
    </div>

    <!-- Condivisione Profilo -->
    <div class="bg-white/5 border border-white/10 rounded-3xl p-6 mb-8 backdrop-blur-md text-white shadow-xl">
      <h2 class="text-xl font-bold mb-2 text-white flex items-center gap-2">
        <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M8.684 10.742l4.828-2.414m0 0a3 3 0 10-3.62-1.09l-4.829 2.414m4.829 2.414a3 3 0 11-3.62 1.09l-4.828-2.414m4.828 2.414a3 3 0 003.62-1.09" />
        </svg>
        Condividi la tua passione
      </h2>
      <p class="text-xs text-gray-400 mb-6 leading-relaxed">
        Il tuo profilo pubblico consente a chiunque di visualizzare i film che hai completato, le tue ore di visione e i tuoi voti personali. 
        Usa i pulsanti sottostanti per copiare il tuo link personale o generare un catalogo PDF.
      </p>
      
      <div class="flex flex-col gap-4">
        <!-- URL Display bar -->
        <div class="flex items-center gap-2 bg-slate-950/40 border border-white/10 rounded-xl px-4 py-2.5 text-xs text-gray-300 font-mono break-all">
          {{ shareUrl }}
        </div>
        
        <div class="flex flex-wrap gap-3">
          <button
            @click="copyShareUrl"
            class="inline-flex items-center gap-2 px-5 py-2.5 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/40 text-purple-300 font-bold rounded-xl text-xs transition cursor-pointer shadow-md shadow-purple-500/5 hover:scale-102"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <span>{{ copied ? 'Copiato!' : 'Copia Link' }}</span>
          </button>

          <a
            :href="shareUrl"
            target="_blank"
            class="inline-flex items-center gap-2 px-5 py-2.5 bg-white/5 hover:bg-white/10 border border-white/10 text-white font-bold rounded-xl text-xs transition cursor-pointer hover:scale-102"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            <span>Vedi Profilo</span>
          </a>

          <a
            :href="shareUrl + '?print=true'"
            target="_blank"
            class="inline-flex items-center gap-2 px-5 py-2.5 bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/40 text-emerald-300 font-bold rounded-xl text-xs transition cursor-pointer hover:scale-102"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
            </svg>
            <span>Genera Catalogo PDF</span>
          </a>
        </div>
      </div>
    </div>

    <!-- Support Card -->
    <div class="bg-gradient-to-br from-purple-600/20 to-pink-600/20 border border-purple-500/30 rounded-3xl p-6 text-white shadow-xl backdrop-blur-md relative overflow-hidden">
      <div class="absolute top-0 right-0 p-4 opacity-5 select-none pointer-events-none">
        <span class="text-9xl">☕</span>
      </div>
      <div class="relative z-10">
        <h2 class="text-2xl font-bold mb-2">Ti piace PopCornNote?</h2>
        <p class="text-gray-300 mb-6 max-w-lg text-sm leading-relaxed">
          Siamo un progetto indipendente e gratuito. Se apprezzi il nostro lavoro, considera di offrirci un caffè per mantenere i server attivi!
        </p>
        <SupportButton label="Offrici un caffè" class="px-5 py-2.5 bg-white text-purple-600 hover:bg-white/95 border-none font-bold rounded-xl text-sm transition cursor-pointer shadow-md" />
      </div>
    </div>

    <!-- Zona Pericolosa -->
    <div class="bg-red-500/5 border border-red-500/20 rounded-3xl p-6 text-white shadow-xl backdrop-blur-md">
      <h2 class="text-xl font-bold mb-4 text-red-400 flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        Zona Pericolosa
      </h2>
      
      <p class="text-xs text-gray-400 mb-6 leading-relaxed">
        Se elimini il tuo account, perderai permanentemente tutti i film, le serie e i dati salvati. Questa azione non può essere annullata in alcun modo.
      </p>

      <button
        @click="showDeleteConfirm = true"
        class="px-5 py-2.5 bg-red-500/20 hover:bg-red-500/30 border border-red-500/40 text-red-300 font-bold rounded-xl text-sm transition cursor-pointer hover:scale-102"
      >
        Elimina Account
      </button>
    </div>

    <!-- Modal Conferma Eliminazione -->
    <div 
      v-if="showDeleteConfirm" 
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
    >
      <div class="bg-slate-900 border border-white/10 rounded-3xl max-w-md w-full p-6 text-center shadow-2xl backdrop-blur-md">
        <div class="mx-auto w-12 h-12 rounded-full bg-red-500/10 border border-red-500/20 flex items-center justify-center mb-4 text-red-400">
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        
        <h3 class="text-xl font-bold mb-2 text-white">Sei assolutamente sicuro?</h3>
        <p class="text-xs text-gray-400 mb-6">
          Stai per eliminare <strong>{{ user?.email }}</strong>. <br/>
          Tutti i dati della tua collezione verranno cancellati per sempre.
        </p>

        <div class="flex gap-3 justify-center">
          <button 
            @click="showDeleteConfirm = false"
            class="px-4 py-2 border border-white/10 rounded-xl hover:bg-white/5 text-gray-300 text-sm font-semibold transition cursor-pointer"
            :disabled="loading"
          >
            Annulla
          </button>
          
          <button 
            @click="deleteAccount"
            class="px-4 py-2 bg-red-500/20 border border-red-500/40 hover:bg-red-500/30 text-red-300 rounded-xl text-sm font-bold transition cursor-pointer flex items-center gap-2"
            :disabled="loading"
          >
            <span v-if="loading" class="animate-spin">⌛</span>
            <span>Sì, elimina tutto</span>
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
definePageMeta({ layout: 'wide' })

const { user, logout } = useAuth()
const { apiFetch } = useApi()
const router = useRouter()
const toast = useToast?.()

const showDeleteConfirm = ref(false)
const loading = ref(false)

const emailPrefix = computed(() => user.value?.email ? user.value.email.split('@')[0] : '')

const shareUrl = computed(() => {
  if (typeof window === 'undefined') return ''
  const name = user.value?.username || emailPrefix.value
  return `${window.location.origin}/share/${encodeURIComponent(name)}`
})

const copied = ref(false)

async function copyShareUrl() {
  try {
    await navigator.clipboard.writeText(shareUrl.value)
    copied.value = true
    toast?.show?.('success', 'Link del profilo copiato negli appunti!')
    setTimeout(() => { copied.value = false }, 2000)
  } catch (e) {
    console.error(e)
    toast?.show?.('error', 'Impossibile copiare il link')
  }
}

async function deleteAccount() {
  loading.value = true
  try {
    await apiFetch('/auth/me', { method: 'DELETE' })
    logout()
    router.push('/login')
    setTimeout(() => {
        window.location.reload()
    }, 100)
  } catch (e) {
    console.error('Delete error', e)
    toast?.show?.('error', 'Errore durante l\'eliminazione dell\'account')
  } finally {
    loading.value = false
    showDeleteConfirm.value = false
  }
}

async function exportJSON() {
  try {
    const list = await apiFetch('/movies/')
    if (list.length === 0) {
      toast?.show?.('error', 'La tua collezione è vuota!')
      return
    }
    const cleanList = list.map(m => {
      const { _id, user_id, ...rest } = m
      return rest
    })
    
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(cleanList, null, 2))
    const downloadAnchor = document.createElement('a')
    downloadAnchor.setAttribute("href", dataStr)
    downloadAnchor.setAttribute("download", "popcorn_note_library.json")
    document.body.appendChild(downloadAnchor)
    downloadAnchor.click()
    downloadAnchor.remove()
    
    toast?.show?.('success', 'JSON scaricato con successo!')
  } catch (e) {
    console.error(e)
    toast?.show?.('error', 'Errore durante l\'esportazione JSON')
  }
}

async function exportCSV() {
  try {
    const list = await apiFetch('/movies/')
    if (list.length === 0) {
      toast?.show?.('error', 'La tua collezione è vuota!')
      return
    }
    
    const headers = ['kind', 'title', 'status', 'release_date', 'release_year', 'director', 'runtime', 'tmdb_id', 'tmdb_vote', 'score', 'liked', 'note']
    const csvRows = []
    csvRows.push(headers.join(','))
    
    for (const m of list) {
      const values = headers.map(header => {
        const val = m[header]
        if (val == null) return ''
        if (typeof val === 'string') {
          const escaped = val.replace(/"/g, '""')
          return `"${escaped}"`
        }
        if (Array.isArray(val)) {
          const escaped = JSON.stringify(val).replace(/"/g, '""')
          return `"${escaped}"`
        }
        return val
      })
      csvRows.push(values.join(','))
    }
    
    const csvContent = "data:text/csv;charset=utf-8," + encodeURIComponent(csvRows.join('\n'))
    const downloadAnchor = document.createElement('a')
    downloadAnchor.setAttribute("href", csvContent)
    downloadAnchor.setAttribute("download", "popcorn_note_library.csv")
    document.body.appendChild(downloadAnchor)
    downloadAnchor.click()
    downloadAnchor.remove()
    
    toast?.show?.('success', 'CSV scaricato con successo!')
  } catch (e) {
    console.error(e)
    toast?.show?.('error', 'Errore durante l\'esportazione CSV')
  }
}
</script>

<style scoped>
</style>
