<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity" @click="$emit('close')"></div>

    <!-- Modal Content -->
    <div class="relative w-full max-w-lg bg-white dark:bg-gray-800 rounded-2xl shadow-2xl overflow-hidden transform transition-all scale-100 p-6 text-center space-y-6">
      
      <!-- Close Button -->
      <button @click="$emit('close')" class="absolute top-4 right-4 p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
      </button>

      <!-- Title -->
      <h2 class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-500 to-pink-500">
        Cosa guardiamo stasera?
      </h2>

      <!-- Content Area -->
      <div class="min-h-[300px] flex flex-col items-center justify-center">
        
        <!-- Loading / Shuffling Animation -->
        <div v-if="loading" class="flex flex-col items-center gap-4">
           <div class="text-6xl animate-bounce">🎲</div>
           <p class="text-lg font-medium text-gray-600 animate-pulse">Lancio i dadi...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="space-y-4">
           <div class="text-5xl">😕</div>
           <p class="text-red-500">{{ error }}</p>
           <button @click="pickRandom" class="px-6 py-2 bg-gray-200 rounded-full hover:bg-gray-300 transition">Riprova</button>
        </div>

        <!-- Result -->
        <div v-else-if="movie" class="w-full space-y-4 animate-fade-in-up">
           
           <div class="relative mx-auto w-48 aspect-[2/3] rounded-lg shadow-lg overflow-hidden group">
             <img v-if="movie.poster_url" :src="movie.poster_url" class="w-full h-full object-cover" />
             <div v-else class="w-full h-full bg-gray-200 flex items-center justify-center text-gray-400">N/A</div>
             
             <!-- Overlay info quick -->
             <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-4">
                <span class="text-white text-sm font-medium">{{ movie.release_year }}</span>
             </div>
           </div>

           <div class="space-y-1">
             <h3 class="text-xl font-bold text-gray-900 dark:text-white">{{ movie.title }}</h3>
             <p class="text-sm text-gray-500">{{ movie.director }}</p>
           </div>
           
           <p v-if="movie.overview" class="text-sm text-gray-600 dark:text-gray-300 line-clamp-3 px-4">
             {{ movie.overview }}
           </p>

           <div class="pt-4 flex flex-col sm:flex-row gap-3 justify-center">
              <NuxtLink 
                :to="movie.kind === 'tv' ? `/tv/${movie.id}` : `/movies/${movie.id}`"
                class="px-6 py-3 bg-gradient-to-r from-emerald-500 to-teal-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl hover:scale-105 transition transform"
              >
                🍿 Guarda ora
              </NuxtLink>
              
              <button 
                @click="pickRandom"
                class="px-6 py-3 bg-white border border-gray-200 text-gray-700 font-medium rounded-xl hover:bg-gray-50 transition"
              >
                🔄 Pesca un altro
              </button>
           </div>

        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['close'])
const { apiFetch } = useApi()

const loading = ref(true)
const movie = ref(null)
const error = ref('')

async function pickRandom() {
  loading.value = true
  error.value = ''
  movie.value = null
  
  // Fake delay for suspense
  await new Promise(r => setTimeout(r, 800))

  try {
    const res = await apiFetch('/movies/random', {
        query: { status: 'to_watch' } // default
    })
    movie.value = res
  } catch (e) {
    if (e.response?.status === 404) {
        error.value = "Nessun titolo 'Da vedere' trovato! Aggiungine qualcuno."
    } else {
        error.value = "Ops, qualcosa è andato storto."
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
    pickRandom()
})
</script>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.5s ease-out forwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
