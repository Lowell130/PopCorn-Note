<!-- pages/share/[username].vue -->
<template>
  <div class="max-w-7xl mx-auto px-6 py-12 text-left">
    
    <!-- Spinner loading state -->
    <div v-if="loading" class="text-center py-32">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500 mx-auto"></div>
      <p class="text-xs text-gray-500 mt-4 font-semibold tracking-wider uppercase">Caricamento profilo...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-32 max-w-md mx-auto">
      <div class="w-16 h-16 bg-red-500/10 border border-red-500/20 text-red-400 rounded-full flex items-center justify-center mb-6 mx-auto shadow-lg shadow-red-500/5">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>
      <h2 class="text-2xl font-bold text-white mb-2">Ops! Profilo non disponibile</h2>
      <p class="text-sm text-gray-400 mb-8">{{ error }}</p>
      <NuxtLink to="/login" class="px-6 py-3 bg-white/5 border border-white/10 hover:bg-white/10 text-white rounded-xl text-sm font-bold transition">
        Accedi a PopCornNote
      </NuxtLink>
    </div>

    <!-- Profile Display -->
    <div v-else class="space-y-8 animate-fade-in">
      
      <!-- Public Header banner -->
      <div class="relative bg-white/5 border border-white/10 rounded-3xl p-8 shadow-xl overflow-hidden backdrop-blur-md">
        <div class="absolute -right-10 -bottom-10 opacity-5 select-none pointer-events-none text-9xl">
          🍿
        </div>
        
        <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div class="space-y-2">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-purple-500/15 border border-purple-500/30 text-purple-300">
              <span class="w-2 h-2 rounded-full bg-purple-400 animate-pulse"></span>
              Profilo Pubblico Condiviso
            </span>
            
            <h1 class="text-4xl md:text-5xl font-black text-white tracking-tight">
              Collezione di <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-sky-400">{{ profile.username }}</span>
            </h1>
            <p class="text-xs text-gray-400 font-medium">
              Sfoglia i titoli visti, le ore dedicate ed i preferiti consigliati da {{ profile.username }}.
            </p>
          </div>
          
          <!-- Logo banner branding link -->
          <NuxtLink to="/" class="flex-shrink-0 flex items-center gap-2 px-5 py-2.5 bg-white/5 hover:bg-white/10 border border-white/10 rounded-2xl transition group">
            <span class="text-lg">🍿</span>
            <span class="text-xs font-bold text-gray-300 group-hover:text-white transition">Crea il tuo account gratis</span>
          </NuxtLink>
        </div>
      </div>

      <!-- KPI Metrics grid -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-white/5 p-5 rounded-2xl border border-blue-500/10 text-left">
           <div class="text-[10px] text-blue-400 font-bold uppercase tracking-wider mb-1">Film Totali</div>
           <div class="text-3xl font-black text-white">{{ profile.total_movies }}</div>
        </div>
        <div class="bg-white/5 p-5 rounded-2xl border border-yellow-500/10 text-left">
           <div class="text-[10px] text-yellow-400 font-bold uppercase tracking-wider mb-1">Serie TV</div>
           <div class="text-3xl font-black text-white">{{ profile.total_series }}</div>
        </div>
        <div class="bg-white/5 p-5 rounded-2xl border border-green-500/10 text-left">
           <div class="text-[10px] text-green-400 font-bold uppercase tracking-wider mb-1">Titoli Visti</div>
           <div class="text-3xl font-black text-white">{{ profile.watched }}</div>
        </div>
        <div class="bg-white/5 p-5 rounded-2xl border border-sky-500/10 text-left">
           <div class="text-[10px] text-sky-400 font-bold uppercase tracking-wider mb-1">Tempo di Visione</div>
           <div class="text-2xl font-black text-white truncate">{{ formattedWatchtime }}</div>
        </div>
      </div>

      <!-- Movies library list section -->
      <div>
        <h3 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
          🎬 Catalogo Film e Serie TV completate
        </h3>
        
        <div v-if="!profile.movies || profile.movies.length === 0" class="text-center py-20 text-gray-500 bg-white/5 border border-white/10 rounded-3xl">
          Nessun film contrassegnato come Visto al momento.
        </div>
        
        <div v-else class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6">
          <div
            v-for="movie in profile.movies"
            :key="movie.id"
            class="group relative bg-white/5 border border-white/10 rounded-2xl overflow-hidden shadow-lg transition hover:scale-103 duration-200"
          >
            <!-- Poster wrapper -->
            <div class="aspect-[2/3] relative overflow-hidden bg-white/5">
              <img
                v-if="movie.poster_url"
                :src="movie.poster_url"
                :alt="movie.title"
                class="w-full h-full object-cover transition duration-300 group-hover:opacity-60"
              />
              <div v-else class="w-full h-full flex items-center justify-center text-gray-500 text-xs">
                Nessun Poster
              </div>

              <!-- Rating Badge (TMDb) -->
              <div v-if="movie.tmdb_vote" class="absolute top-2 left-2 px-2 py-0.5 rounded-lg bg-black/60 backdrop-blur-xs text-[10px] font-bold text-amber-400 border border-white/10">
                ★ {{ movie.tmdb_vote.toFixed(1) }}
              </div>

              <!-- Media kind label badge -->
              <div class="absolute top-2 right-2 px-2 py-0.5 rounded-lg bg-black/60 backdrop-blur-xs text-[10px] font-bold border"
                :class="movie.kind === 'tv' ? 'border-yellow-500/35 text-yellow-400' : 'border-blue-500/35 text-blue-400'"
              >
                {{ movie.kind === 'tv' ? 'SERIE' : 'FILM' }}
              </div>

              <!-- Hover overlay text descriptor -->
              <div class="absolute inset-x-0 bottom-0 p-4 bg-gradient-to-t from-black/95 via-black/70 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex flex-col justify-end min-h-[60%] text-left">
                <h4 class="font-bold text-white text-xs line-clamp-2">{{ movie.title }}</h4>
                <p class="text-[10px] text-gray-400 mt-1">
                  Anno: {{ movie.release_year || '—' }} <span v-if="movie.runtime">· {{ movie.runtime }} min</span>
                </p>
                <div v-if="movie.director" class="text-[9px] text-gray-400 mt-1 line-clamp-1">
                  Regia: <span class="text-white font-medium">{{ movie.director }}</span>
                </div>
                <p v-if="movie.overview" class="text-[9px] text-gray-400 mt-2 line-clamp-3 leading-relaxed">
                  {{ movie.overview }}
                </p>
              </div>
            </div>
            
            <!-- Read-only metadata box -->
            <div class="p-3 text-left border-t border-white/5 bg-slate-950/20">
              <div class="flex items-center justify-between gap-1 text-[10px]">
                <span class="text-gray-500">Voto personale:</span>
                <span class="font-bold text-white">{{ movie.score ? `${movie.score}/10` : '—' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
definePageMeta({ layout: 'wide' })

const route = useRoute()
const username = route.params.username
const { apiFetch } = useApi()

const loading = ref(true)
const profile = ref(null)
const error = ref('')

onMounted(async () => {
  try {
    profile.value = await apiFetch(`/social/profile/${username}`)
    if (route.query.print === 'true') {
      // Attendi il caricamento delle immagini caricate in modo eager
      setTimeout(() => {
        window.print()
      }, 3000)
    }
  } catch (e) {
    console.error(e)
    error.value = e?.response?._data?.detail || 'Profilo utente non trovato o inesistente'
  } finally {
    loading.value = false
  }
})

const formattedWatchtime = computed(() => {
  const mins = profile.value?.total_watchtime || 0
  if (mins === 0) return '0m'
  const days = Math.floor(mins / 1440)
  const hours = Math.floor((mins % 1440) / 60)
  const remainingMins = mins % 60
  
  const parts = []
  if (days > 0) parts.push(`${days}g`)
  if (hours > 0) parts.push(`${hours}h`)
  if (remainingMins > 0 || parts.length === 0) parts.push(`${remainingMins}m`)
  return parts.join(' ')
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

<style>
/* Global print overrides to hide layout wrappers and ensure text is visible on paper */
@media print {
  header, footer, nav, button, a.flex-shrink-0,
  #__nuxt header, #__nuxt footer, #__nuxt nav, [role="navigation"] {
    display: none !important;
  }
  
  body, html, main, #__nuxt {
    background: #ffffff !important;
    color: #000000 !important;
  }

  /* Fixes text transparency (gradient text) in print preview */
  span.text-transparent {
    color: #6d28d9 !important; /* dark purple */
    -webkit-text-fill-color: #6d28d9 !important;
    background: none !important;
  }

  .bg-white\/5 {
    background: #f9fafb !important;
    border: 1px solid #e5e7eb !important;
    color: #111827 !important;
    box-shadow: none !important;
  }
  
  .text-white {
    color: #111827 !important;
  }
  
  .text-gray-400, .text-gray-500 {
    color: #374151 !important;
  }
  
  .grid {
    display: grid !important;
    grid-template-cols: repeat(3, minmax(0, 1fr)) !important;
    gap: 1.5rem !important;
  }
  
  .group {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }
}
</style>
