<template>
  <div class="max-w-6xl mx-auto py-10 px-4 space-y-10">
    
    <!-- Header Hero -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-gray-200 dark:border-gray-700 pb-6">
      <div>
         <h2 class="text-sm font-semibold text-blue-600 dark:text-blue-400 uppercase tracking-wider mb-1">
            Analytics
         </h2>
         <h1 class="text-4xl font-extrabold text-gray-900 dark:text-white">
            Le tue Statistiche
         </h1>
         <p class="text-gray-500 dark:text-gray-400 mt-2">
            Analizza le tue abitudini di visione e scopri cosa ti piace davvero.
         </p>
      </div>
      
      <NuxtLink 
        to="/" 
        class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-700 transition"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
        Torna alla Dashboard
      </NuxtLink>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-32 space-y-4 text-gray-500">
      <Spinner class="w-12 h-12" />
      <span class="text-sm font-medium animate-pulse">Analizzo i dati...</span>
    </div>

    <!-- Content -->
    <div v-else-if="stats && stats.stats_advanced" class="space-y-8 animate-fade-in-up">
      
      <!-- KPI Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 p-5 rounded-2xl shadow-sm border border-blue-100 dark:border-blue-800">
           <div class="text-xs text-blue-600 dark:text-blue-300 font-bold uppercase mb-1">Film Totali</div>
           <div class="text-3xl font-bold text-gray-900 dark:text-white">{{ stats.total_movies }}</div>
        </div>
        <div class="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 p-5 rounded-2xl shadow-sm border border-green-100 dark:border-green-800">
           <div class="text-xs text-green-600 dark:text-green-300 font-bold uppercase mb-1">Visti</div>
           <div class="text-3xl font-bold text-gray-900 dark:text-white">{{ stats.watched }}</div>
        </div>
        <div class="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 p-5 rounded-2xl shadow-sm border border-purple-100 dark:border-purple-800">
           <div class="text-xs text-purple-600 dark:text-purple-300 font-bold uppercase mb-1">Da Vedere</div>
           <div class="text-3xl font-bold text-gray-900 dark:text-white">{{ stats.to_watch }}</div>
        </div>
        <div class="bg-gradient-to-br from-amber-50 to-amber-100 dark:from-amber-900/20 dark:to-amber-800/20 p-5 rounded-2xl shadow-sm border border-amber-100 dark:border-amber-800">
           <div class="text-xs text-amber-600 dark:text-amber-300 font-bold uppercase mb-1">Score Medio</div>
           <div class="text-3xl font-bold text-gray-900 dark:text-white">{{ stats.avg_score || '—' }}</div>
        </div>
      </div>

      <!-- Charts Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        <!-- Top Registi -->
        <div class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 flex flex-col">
          <div class="mb-6">
            <h3 class="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <span class="text-2xl">🎬</span> Registi Preferiti
            </h3>
            <p class="text-sm text-gray-500 mt-1">I registi che compaiono più spesso nella tua lista.</p>
          </div>
          <div class="flex-1 min-h-[300px] relative">
             <BarChart v-if="directorsData" :chart-data="directorsData" :chart-options="barOptions" />
             <div v-else class="absolute inset-0 flex items-center justify-center text-gray-400 text-sm">Nessun dato disponibile</div>
          </div>
        </div>

        <!-- Anni di Rilascio -->
        <div class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 flex flex-col">
          <div class="mb-6">
            <h3 class="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <span class="text-2xl">🗓️</span> Timeline
            </h3>
            <p class="text-sm text-gray-500 mt-1">Distribuzione dei film per decennio.</p>
          </div>
          <div class="flex-1 min-h-[300px] relative">
             <BarChart v-if="yearsData" :chart-data="yearsData" :chart-options="barOptions" />
             <div v-else class="absolute inset-0 flex items-center justify-center text-gray-400 text-sm">Nessun dato disponibile</div>
          </div>
        </div>

        <!-- Voti Distribuzione (Full width on mobile, half on large if needed, keeping simple grid for now) -->
        <div class="lg:col-span-2 bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700">
          <div class="grid md:grid-cols-2 gap-10 items-center">
              <div>
                   <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">
                      ⭐ Come valuti?
                   </h3>
                   <p class="text-gray-600 dark:text-gray-300 leading-relaxed mb-6">
                      Questa distribuzione mostra quanto sei critico o generoso. 
                      Una curva spostata verso destra indica che tendi a goderti ciò che guardi!
                   </p>
                   
                   <div class="bg-gray-50 dark:bg-gray-900 p-4 rounded-xl border border-gray-100 dark:border-gray-800">
                       <span class="text-sm text-gray-500 block mb-1">Voto più frequente</span>
                       <div class="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
                          {{ mostFrequentScore.score ? `${mostFrequentScore.score}/10` : '—' }}
                       </div>
                       <div class="text-xs text-gray-400 mt-1">
                          Assegnato {{ mostFrequentScore.count }} volte
                       </div>
                   </div>
              </div>
              <div class="h-[300px] flex justify-center items-center relative">
                   <DoughnutChart v-if="scoresData" :chart-data="scoresData" :chart-options="doutOptions" />
                   <div v-else class="text-gray-400 text-sm">Nessun voto assegnato</div>
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

const directorsData = ref(null)
const yearsData = ref(null)
const scoresData = ref(null)
const mostFrequentScore = ref({ score: null, count: 0 })

const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        y: { beginAtZero: true, grid: { color: '#f3f4f6' } },
        x: { grid: { display: false } }
    },
    plugins: {
        legend: { display: false } 
    }
}
const doutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { position: 'bottom', labels: { padding: 20, usePointStyle: true } }
    }
}

onMounted(async () => {
    // Fake delay per mostrare lo spinner figo (rimuovi in prod se vuoi)
    // await new Promise(r => setTimeout(r, 1000)) 
    
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
                backgroundColor: '#3b82f6', // blue-500
                hoverBackgroundColor: '#2563eb',
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
                backgroundColor: '#8b5cf6', // violet-500
                hoverBackgroundColor: '#7c3aed',
                data: sortedDecades.map(d => decades[d]),
                borderRadius: 8,
                barThickness: 30,
            }]
        }
    }

    // 3. Scores
    const scores = adv.scores || []
    if (scores.length) {
        // Find frequent
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
                    '#ef4444', '#f87171', '#fca5a5', 
                    '#fbbf24', '#fcd34d', '#fde047', 
                    '#34d399', '#10b981', '#059669', '#047857'
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
