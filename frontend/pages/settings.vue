<template>
  <div class="max-w-2xl mx-auto py-8">
    <h1 class="text-3xl font-bold mb-8">Impostazioni</h1>

    <!-- Profilo Card -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Il tuo Profilo</h2>
      
      <div v-if="user" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-500">Email</label>
          <div class="mt-1 text-lg">{{ user.email }}</div>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-500">Username</label>
          <div class="mt-1 text-lg">{{ user.username || '—' }}</div>
        </div>
      </div>
    </div>

    <!-- Support Card -->
    <div class="bg-gradient-to-br from-pink-500 to-rose-600 rounded-xl shadow-lg p-6 mb-8 text-white relative overflow-hidden">
      <div class="absolute top-0 right-0 p-4 opacity-10">
        <span class="text-9xl">☕</span>
      </div>
      <div class="relative z-10">
        <h2 class="text-2xl font-bold mb-2">Ti piace PopCornNote?</h2>
        <p class="text-pink-100 mb-6 max-w-lg text-lg">
          Siamo un progetto indipendente e gratuito. Se apprezzi il nostro lavoro, considera di offrirci un caffè per mantenere i server attivi!
        </p>
        <SupportButton label="Offrici un caffè" class="bg-white text-pink-600 hover:bg-pink-50 hover:text-pink-700 border-none" />
      </div>
    </div>

    <!-- Zona Pericolosa -->
    <div class="bg-red-50 dark:bg-red-900/10 border border-red-100 dark:border-red-900/30 rounded-xl shadow p-6">
      <h2 class="text-xl font-semibold mb-4 text-red-600 dark:text-red-400">Zona Pericolosa</h2>
      
      <p class="text-sm text-gray-600 dark:text-gray-400 mb-6">
        Se elimini il tuo account, perderai permanentemente tutti i film, le serie e i dati salvati. Questa azione non può essere annullata.
      </p>

      <button
        @click="showDeleteConfirm = true"
        class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 focus:ring-4 focus:ring-red-300 transition-colors"
      >
        Elimina Account
      </button>
    </div>

    <!-- Modal Conferma Eliminazione -->
    <div 
      v-if="showDeleteConfirm" 
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
    >
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-md w-full p-6 text-center">
        <div class="mx-auto w-12 h-12 rounded-full bg-red-100 flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        
        <h3 class="text-xl font-bold mb-2">Sei assolutamente sicuro?</h3>
        <p class="text-sm text-gray-500 mb-6">
          Stai per eliminare <strong>{{ user?.email }}</strong>. <br/>
          Tutti i dati verranno cancellati per sempre.
        </p>

        <div class="flex gap-3 justify-center">
          <button 
            @click="showDeleteConfirm = false"
            class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-gray-700"
            :disabled="loading"
          >
            Annulla
          </button>
          
          <button 
            @click="deleteAccount"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 flex items-center gap-2"
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

async function deleteAccount() {
  loading.value = true
  try {
    await apiFetch('/auth/me', { method: 'DELETE' })
    
    // Logout e redirect
    logout() // pulisce il token
    router.push('/login')
    
    // Piccolo hack: reload per pulire states
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
</script>
