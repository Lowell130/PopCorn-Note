<!-- components/DashboardStats.vue -->
<template>
  <!-- <div class="bg-white text-black rounded-xl p-4 shadow text-sm mb-4"> -->
    <div class="bg-white text-black text-sm mb-4">
    <p class="flex flex-wrap gap-x-4 gap-y-2">
      <span class="bg-blue-100 text-blue-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm dark:bg-blue-900 dark:text-blue-300">{{ mTotalMovies }} film</span>
      <span class="bg-yellow-100 text-yellow-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm dark:bg-yellow-900 dark:text-yellow-300">{{ mTotalSeries }} serie</span>
      <span class="bg-purple-100 text-purple-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm dark:bg-purple-900 dark:text-purple-300">{{ mWatched }} visti</span>
      <span class="bg-green-100 text-green-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm dark:bg-green-900 dark:text-green-300">{{ mToWatch }} da vedere</span>
      <span class="bg-red-100 text-red-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm dark:bg-red-900 dark:text-red-300">{{ mAvgScore }} score medio</span>
    </p>
  </div>
</template>

<script setup>
const props = defineProps({
  // nuovo: stats calcolate lato backend
  stats: { type: Object, default: null },
  // fallback: vecchio comportamento
  movies: { type: Array, default: () => [] }
})

const fromStats = computed(() => !!props.stats)

// valori dal backend (se disponibili)
const mTotalMovies = computed(() =>
  fromStats.value ? props.stats.total_movies : props.movies.filter(m => m.kind === 'movie' || !('kind' in m)).length
)
const mTotalSeries = computed(() =>
  fromStats.value ? props.stats.total_series : props.movies.filter(m => m.kind === 'tv').length
)
const mWatched = computed(() =>
  fromStats.value ? props.stats.watched : props.movies.filter(m => m.status === 'watched').length
)
const mToWatch = computed(() =>
  fromStats.value ? props.stats.to_watch : props.movies.filter(m => m.status === 'to_watch').length
)
const mAvgScore = computed(() => {
  if (fromStats.value) return props.stats.avg_score ?? '—'
  const arr = props.movies.map(m => m.score).filter(n => typeof n === 'number')
  if (!arr.length) return '—'
  return (arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(1)
})
</script>
