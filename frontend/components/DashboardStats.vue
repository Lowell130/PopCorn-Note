<template>
  <div class="grid sm:grid-cols-3 gap-3 mb-6">
    <div class="bg-white text-black rounded-xl p-4 shadow">
      <div class="text-sm opacity-70">Totale film</div>
      <div class="text-2xl font-semibold">{{ total }}</div>
    </div>
    <div class="bg-white text-black rounded-xl p-4 shadow">
      <div class="text-sm opacity-70">Visti</div>
      <div class="text-2xl font-semibold">{{ watched }}</div>
    </div>
    <div class="bg-white text-black rounded-xl p-4 shadow">
      <div class="text-sm opacity-70">Da vedere</div>
      <div class="text-2xl font-semibold">{{ to_watch }}</div>
    </div>
    <!-- <div class="bg-white text-black rounded-xl p-4 shadow">
      <div class="text-sm opacity-70">Media score</div>
      <div class="text-2xl font-semibold">{{ avgScore }}</div>
    </div> -->
  </div>
</template>

<script setup>
const props = defineProps({ movies: { type: Array, required: true } })
const total = computed(() => props.movies.length)
const watched = computed(() => props.movies.filter(m => m.status === 'watched').length)
const to_watch = computed(() => props.movies.filter(m => m.status === 'to_watch').length)
const avgScore = computed(() => {
  const arr = props.movies.map(m => m.score).filter(n => typeof n === 'number')
  if (!arr.length) return '—'
  const v = arr.reduce((a,b)=>a+b,0)/arr.length
  return v.toFixed(1)
})
</script>
