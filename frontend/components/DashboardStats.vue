<template>
  <div class="bg-white text-black rounded-xl p-4 shadow text-sm mb-4">
    <p class="flex flex-wrap gap-x-4 gap-y-2">
      <span><span class="font-semibold">{{ totalMovies }}</span> film</span>
      <span><span class="font-semibold">{{ totalSeries }}</span> serie</span>
      <span><span class="font-semibold">{{ watched }}</span> visti</span>
      <span><span class="font-semibold">{{ to_watch }}</span> da vedere</span>
      <span><span class="font-semibold">{{ avgScore }}</span> score medio</span>
    </p>
  </div>
</template>

<script setup>
const props = defineProps({ movies: { type: Array, required: true } })

const totalMovies = computed(() => props.movies.filter(m => m.kind === 'movie').length)
const totalSeries = computed(() => props.movies.filter(m => m.kind === 'tv').length)

const watched = computed(() => props.movies.filter(m => m.status === 'watched').length)
const to_watch = computed(() => props.movies.filter(m => m.status === 'to_watch').length)

const avgScore = computed(() => {
  const arr = props.movies.map(m => m.score).filter(n => typeof n === 'number')
  if (!arr.length) return '—'
  return (arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(1)
})
</script>
