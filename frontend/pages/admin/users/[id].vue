<!-- pages/admin/users/[id].vue -->
<template>
  <div class="bg-white text-black rounded-2xl p-5 shadow space-y-4">
    <NuxtLink to="/admin/users" class="text-sm text-blue-700 hover:underline">← Back</NuxtLink>
    <h1 class="text-2xl font-semibold">User stats</h1>

    <div v-if="loading">Loading…</div>
    <div v-else class="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
      <div class="p-3 rounded border">Movies: <b>{{ stats.total_movies }}</b></div>
      <div class="p-3 rounded border">Series: <b>{{ stats.total_series }}</b></div>
      <div class="p-3 rounded border">Watching: <b>{{ stats.watching }}</b></div>
      <div class="p-3 rounded border">To watch: <b>{{ stats.to_watch }}</b></div>
      <div class="p-3 rounded border">Watched: <b>{{ stats.watched }}</b></div>
      <div class="p-3 rounded border">Upcoming: <b>{{ stats.upcoming }}</b></div>
      <div class="p-3 rounded border">Avg score: <b>{{ stats.avg_score ?? '—' }}</b></div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ middleware: 'admin-only' })
const route = useRoute()
const { apiFetch } = useApi()
const stats = ref({})
const loading = ref(true)

onMounted(async () => {
  try { stats.value = await apiFetch(`/admin/users/${route.params.id}/stats`) }
  finally { loading.value = false }
})
</script>
