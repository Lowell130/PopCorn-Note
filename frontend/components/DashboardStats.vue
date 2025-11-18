<template>
  <div class="text-black text-sm mb-4">
    <p class="text-xs font-semibold text-gray-500 mb-2">Statistiche libreria</p>

    <div class="space-y-3">
      <!-- Riga: Film -->
      <div>
        <div class="flex items-center justify-between text-xs mb-1">
          <span class="text-gray-600">Film</span>
          <span class="font-medium">{{ mTotalMovies }}</span>
        </div>
        <div class="h-2 rounded-full bg-gray-100 overflow-hidden">
          <div
            class="h-full rounded-full bg-blue-500 transition-all"
            :style="{ width: moviesPct + '%' }"
          ></div>
        </div>
      </div>

      <!-- Riga: Serie -->
      <div>
        <div class="flex items-center justify-between text-xs mb-1">
          <span class="text-gray-600">Serie</span>
          <span class="font-medium">{{ mTotalSeries }}</span>
        </div>
        <div class="h-2 rounded-full bg-gray-100 overflow-hidden">
          <div
            class="h-full rounded-full bg-yellow-500 transition-all"
            :style="{ width: seriesPct + '%' }"
          ></div>
        </div>
      </div>

      <!-- Riga: Visti -->
      <div>
        <div class="flex items-center justify-between text-xs mb-1">
          <span class="text-gray-600">Visti</span>
          <span class="font-medium">{{ mWatched }}</span>
        </div>
        <div class="h-2 rounded-full bg-gray-100 overflow-hidden">
          <div
            class="h-full rounded-full bg-purple-500 transition-all"
            :style="{ width: watchedPct + '%' }"
          ></div>
        </div>
      </div>

      <!-- Riga: Da vedere -->
      <div>
        <div class="flex items-center justify-between text-xs mb-1">
          <span class="text-gray-600">Da vedere</span>
          <span class="font-medium">{{ mToWatch }}</span>
        </div>
        <div class="h-2 rounded-full bg-gray-100 overflow-hidden">
          <div
            class="h-full rounded-full bg-green-500 transition-all"
            :style="{ width: toWatchPct + '%' }"
          ></div>
        </div>
      </div>

      <!-- Riga: Score medio -->
      <div class="pt-1 border-t border-gray-100 mt-1">
        <div class="flex items-center justify-between text-xs mb-1">
          <span class="text-gray-600 flex items-center gap-1">
            <svg
              class="w-3.5 h-3.5 text-yellow-400"
              viewBox="0 0 20 20"
              fill="currentColor"
              aria-hidden="true"
            >
              <path
                d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81H7.03a1 1 0 00.95-.69l1.07-3.292z"
              />
            </svg>
            Score medio
          </span>
          <span class="font-medium">
            {{ mAvgScoreLabel }}
          </span>
        </div>
        <div class="h-2 rounded-full bg-gray-100 overflow-hidden">
          <div
            class="h-full rounded-full bg-red-500 transition-all"
            :style="{ width: avgScorePct + '%' }"
          ></div>
        </div>
      </div>
    </div>
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
  fromStats.value
    ? props.stats.total_movies
    : props.movies.filter(m => m.kind === 'movie' || !('kind' in m)).length
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

// score medio
const mAvgScore = computed(() => {
  if (fromStats.value) return props.stats.avg_score ?? null
  const arr = props.movies.map(m => m.score).filter(n => typeof n === 'number')
  if (!arr.length) return null
  return +(arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(1)
})
const mAvgScoreLabel = computed(() => (mAvgScore.value == null ? '—' : `${mAvgScore.value}/10`))

// normalizzazione per barre (in base al valore massimo)
const maxCount = computed(() => {
  return Math.max(
    1,
    mTotalMovies.value || 0,
    mTotalSeries.value || 0,
    mWatched.value || 0,
    mToWatch.value || 0
  )
})

const moviesPct = computed(() => Math.round(((mTotalMovies.value || 0) / maxCount.value) * 100))
const seriesPct = computed(() => Math.round(((mTotalSeries.value || 0) / maxCount.value) * 100))
const watchedPct = computed(() => Math.round(((mWatched.value || 0) / maxCount.value) * 100))
const toWatchPct = computed(() => Math.round(((mToWatch.value || 0) / maxCount.value) * 100))

// score medio in % su base 10
const avgScorePct = computed(() => {
  if (mAvgScore.value == null) return 0
  return Math.max(0, Math.min(100, (mAvgScore.value / 10) * 100))
})
</script>
