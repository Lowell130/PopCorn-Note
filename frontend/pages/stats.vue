<template>
  <div class="max-w-6xl mx-auto py-10 px-4 space-y-8">
    
    <!-- Header Hero -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-white/10 pb-6">
      <div>
         <h2 class="text-sm font-semibold text-purple-400 uppercase tracking-wider mb-1">
            Analytics
         </h2>
         <h1 class="text-4xl font-extrabold text-white tracking-tight">
            Le tue Statistiche
         </h1>
         <p class="text-gray-400 mt-2">
            Analizza le tue abitudini di visione e scopri cosa ti piace davvero.
         </p>
      </div>
      
      <NuxtLink 
        to="/dashboard" 
        class="inline-flex items-center gap-2 px-4 py-2.5 text-sm font-semibold text-gray-300 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition hover:scale-102 duration-150 shadow-md"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
        Torna alla Dashboard
      </NuxtLink>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-32 space-y-4 text-gray-400">
      <Spinner class="w-12 h-12" />
      <span class="text-sm font-medium animate-pulse">Analizzo i dati...</span>
    </div>

    <!-- Content -->
    <div v-else-if="stats && stats.stats_advanced" class="space-y-8 animate-fade-in-up">
      
      <!-- Guide Banner (Explain how stats are populated) -->
      <div class="bg-purple-950/20 border border-purple-500/30 p-6 rounded-2xl flex items-start gap-4 shadow-xl backdrop-blur-md">
        <div class="p-3 bg-purple-500/10 border border-purple-500/20 rounded-xl text-purple-300 flex-shrink-0 select-none">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div class="space-y-1 text-left">
          <h4 class="text-sm font-bold text-white">Come viene alimentata questa pagina?</h4>
          <p class="text-xs text-gray-300 leading-relaxed">
            I grafici e i contatori si aggiornano in tempo reale in base ai titoli presenti nella tua Dashboard. 
            Cliccando sull'icona di modifica (la matita <span class="text-purple-400 font-semibold">📝</span>) su qualsiasi scheda di film o serie, 
            potrai inserire i tuoi voti personali (da 1 a 10), impostare lo stato di visione (Visto, In Visione, Da Vedere) ed esprimere il tuo gradimento. 
            Il nostro motore di reportistica analizzerà istantaneamente le tue risposte per produrre le statistiche qui sotto.
          </p>
        </div>
      </div>

      <!-- KPI Cards -->
      <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div class="bg-white/5 p-5 rounded-2xl shadow-sm border border-blue-500/20 text-left">
           <div class="text-xs text-blue-400 font-bold uppercase mb-1">Film Totali</div>
           <div class="text-3xl font-black text-white">{{ stats.total_movies }}</div>
        </div>
        <div class="bg-white/5 p-5 rounded-2xl shadow-sm border border-green-500/20 text-left">
           <div class="text-xs text-green-400 font-bold uppercase mb-1">Visti</div>
           <div class="text-3xl font-black text-white">{{ stats.watched }}</div>
        </div>
        <div class="bg-white/5 p-5 rounded-2xl shadow-sm border border-purple-500/20 text-left">
           <div class="text-xs text-purple-400 font-bold uppercase mb-1">Da Vedere</div>
           <div class="text-3xl font-black text-white">{{ stats.to_watch }}</div>
        </div>
        <div class="bg-white/5 p-5 rounded-2xl shadow-sm border border-sky-500/20 text-left">
           <div class="text-xs text-sky-400 font-bold uppercase mb-1">Tempo di Visione</div>
           <div class="text-2xl sm:text-3xl font-black text-white truncate">{{ formattedWatchtime }}</div>
        </div>
        <div class="bg-white/5 p-5 rounded-2xl shadow-sm border border-amber-500/20 text-left">
           <div class="text-xs text-amber-400 font-bold uppercase mb-1">Score Medio</div>
           <div class="text-3xl font-black text-white">{{ stats.avg_score || '—' }}</div>
        </div>
      </div>

      <!-- Charts Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        <!-- Top Registi -->
        <div class="bg-white/5 border border-white/10 p-6 rounded-3xl shadow-xl flex flex-col backdrop-blur-md text-left">
          <div class="mb-6 flex items-start gap-3">
            <div class="p-2 bg-purple-500/10 border border-purple-500/20 rounded-lg text-purple-300 flex-shrink-0">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-white">Registi Preferiti</h3>
              <p class="text-xs text-gray-400 mt-0.5">I registi che compaiono più spesso nella tua lista.</p>
            </div>
          </div>
          <div class="flex-1 min-h-[300px] relative">
             <BarChart v-if="directorsData" :chart-data="directorsData" :chart-options="barOptions" />
             <div v-else class="absolute inset-0 flex items-center justify-center text-gray-500 text-sm">Nessun dato disponibile</div>
          </div>
        </div>

        <!-- Anni di Rilascio -->
        <div class="bg-white/5 border border-white/10 p-6 rounded-3xl shadow-xl flex flex-col backdrop-blur-md text-left">
          <div class="mb-6 flex items-start gap-3">
            <div class="p-2 bg-sky-500/10 border border-sky-500/20 rounded-lg text-sky-300 flex-shrink-0">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-white">Timeline decenni</h3>
              <p class="text-xs text-gray-400 mt-0.5">Distribuzione dei titoli salvati per anno di rilascio.</p>
            </div>
          </div>
          <div class="flex-1 min-h-[300px] relative">
             <BarChart v-if="yearsData" :chart-data="yearsData" :chart-options="barOptions" />
             <div v-else class="absolute inset-0 flex items-center justify-center text-gray-500 text-sm">Nessun dato disponibile</div>
          </div>
        </div>

        <!-- Voti Distribuzione -->
        <div class="lg:col-span-2 bg-white/5 border border-white/10 p-8 rounded-3xl shadow-xl backdrop-blur-md text-left">
          <div class="grid md:grid-cols-2 gap-10 items-center">
              <div>
                   <div class="flex items-center gap-3 mb-3">
                     <div class="p-2 bg-amber-500/10 border border-amber-500/20 rounded-lg text-amber-300 flex-shrink-0">
                       <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                         <path stroke-linecap="round" stroke-linejoin="round" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                       </svg>
                     </div>
                     <h3 class="text-xl font-bold text-white">
                        Curva di gradimento
                     </h3>
                   </div>
                   
                   <p class="text-gray-300 text-sm leading-relaxed mb-6">
                      Questa distribuzione analizza la frequenza dei tuoi voti personali. 
                      Una curva spostata verso destra e incentrata sui punteggi più alti indica una preferenza per film e serie TV di qualità che hai gradito maggiormente.
                   </p>
                   
                   <div class="bg-white/5 border border-white/5 p-4 rounded-2xl flex items-center justify-between">
                        <div>
                          <span class="text-xs text-gray-400 block mb-1">Voto più frequente</span>
                          <div class="text-2xl font-black text-purple-400">
                             {{ mostFrequentScore.score ? `${mostFrequentScore.score}/10` : '—' }}
                          </div>
                        </div>
                        <div class="text-right">
                          <span class="text-xs text-gray-500 block">Frequenza</span>
                          <span class="text-sm font-bold text-white">{{ mostFrequentScore.count }} assegnazioni</span>
                        </div>
                   </div>
              </div>
              <div class="h-[300px] flex justify-center items-center relative">
                   <DoughnutChart v-if="scoresData" :chart-data="scoresData" :chart-options="doutOptions" />
                   <div v-else class="text-gray-500 text-sm">Nessun voto assegnato</div>
              </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import Spinner from '@/components/Spinner.vue'
import BarChart from '@/components/charts/BarChart.vue'
import DoughnutChart from '@/components/charts/DoughnutChart.vue'

definePageMeta({ layout: 'wide' })
const { apiFetch } = useApi()

const loading = ref(true)
const stats = ref(null)

const formattedWatchtime = computed(() => {
  const mins = stats.value?.total_watchtime || 0
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

const directorsData = ref(null)
const yearsData = ref(null)
const scoresData = ref(null)
const mostFrequentScore = ref({ score: null, count: 0 })

const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        y: { 
            beginAtZero: true, 
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#9ca3af' }
        },
        x: { 
            grid: { display: false },
            ticks: { color: '#9ca3af' }
        }
    },
    plugins: {
        legend: { display: false } 
    }
}
const doutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { 
            position: 'bottom', 
            labels: { 
                padding: 20, 
                usePointStyle: true,
                color: '#d1d5db'
            } 
        }
    }
}

onMounted(async () => {
  try {
    const res = await apiFetch('/movies/stats')
    stats.value = res
    prepareCharts(res.stats_advanced)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

function prepareCharts(adv) {
    // 1. Directors
    const dirs = adv.directors || []
    if (dirs.length) {
        directorsData.value = {
            labels: dirs.map(d => d.name),
            datasets: [{
                label: 'Film visti',
                backgroundColor: '#a855f7', // purple-500
                hoverBackgroundColor: '#c084fc', // purple-400
                data: dirs.map(d => d.count),
                borderRadius: 8,
                barThickness: 30,
            }]
        }
    }

    // 2. Years
    const rawYears = adv.years || []
    if (rawYears.length) {
        const decades = {}
        rawYears.forEach(item => {
            if (!item.year) return
            const dec = Math.floor(item.year / 10) * 10
            decades[dec] = (decades[dec] || 0) + item.count
        })
        const sortedDecades = Object.keys(decades).sort()
        
        yearsData.value = {
            labels: sortedDecades.map(d => `${d}s`),
            datasets: [{
                label: 'Film',
                backgroundColor: '#0ea5e9', // sky-500
                hoverBackgroundColor: '#38bdf8', // sky-400
                data: sortedDecades.map(d => decades[d]),
                borderRadius: 8,
                barThickness: 30,
            }]
        }
    }

    // 3. Scores (Sophisticated Indigo/Purple palette)
    const scores = adv.scores || []
    if (scores.length) {
        let max = { score: null, count: -1 }
        scores.forEach(s => {
            if (s.count > max.count) max = s
        })
        mostFrequentScore.value = max
        
        const scoreMap = {}
        scores.forEach(s => scoreMap[s.score] = s.count)
        
        const labels = [1,2,3,4,5,6,7,8,9,10]
        scoresData.value = {
            labels: labels.map(s => `Voto ${s}`),
            datasets: [{
                backgroundColor: [
                  '#4f46e5', '#6366f1', '#818cf8', '#a5b4fc', 
                  '#c7d2fe', '#a855f7', '#c084fc', '#d8b4fe', 
                  '#e9d5ff', '#38bdf8'
                ],
                borderWidth: 0,
                data: labels.map(s => scoreMap[s] || 0)
            }]
        }
    }
}
</script>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
