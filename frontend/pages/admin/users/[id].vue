<template>
  <div class="bg-white/5 border border-white/10 text-white rounded-3xl p-8 shadow-2xl space-y-6 backdrop-blur-md">
    <NuxtLink to="/admin/users" class="text-sm font-semibold text-purple-400 hover:text-purple-300 transition-colors">← Back to User Management</NuxtLink>
    <h1 class="text-3xl font-extrabold text-white tracking-tight">Dettaglio statistiche utente</h1>

    <div v-if="loading" class="text-gray-400 animate-pulse text-sm">Caricamento…</div>
    <div v-else class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div class="p-4 rounded-xl bg-white/5 border border-white/5 text-gray-300 text-sm flex justify-between items-center">
        <span>Film Totali:</span>
        <b class="text-white font-bold text-base">{{ stats.total_movies }}</b>
      </div>
      <div class="p-4 rounded-xl bg-white/5 border border-white/5 text-gray-300 text-sm flex justify-between items-center">
        <span>Serie TV:</span>
        <b class="text-white font-bold text-base">{{ stats.total_series }}</b>
      </div>
      <div class="p-4 rounded-xl bg-white/5 border border-white/5 text-gray-300 text-sm flex justify-between items-center">
        <span>In visione:</span>
        <b class="text-white font-bold text-base">{{ stats.watching }}</b>
      </div>
      <div class="p-4 rounded-xl bg-white/5 border border-white/5 text-gray-300 text-sm flex justify-between items-center">
        <span>Da vedere:</span>
        <b class="text-white font-bold text-base">{{ stats.to_watch }}</b>
      </div>
      <div class="p-4 rounded-xl bg-white/5 border border-white/5 text-gray-300 text-sm flex justify-between items-center">
        <span>Visti:</span>
        <b class="text-white font-bold text-base">{{ stats.watched }}</b>
      </div>
      <div class="p-4 rounded-xl bg-white/5 border border-white/5 text-gray-300 text-sm flex justify-between items-center">
        <span>In uscita:</span>
        <b class="text-white font-bold text-base">{{ stats.upcoming }}</b>
      </div>
      <div class="p-4 rounded-xl bg-white/5 border border-white/5 text-gray-300 text-sm flex justify-between items-center col-span-full lg:col-span-1">
        <span>Score medio:</span>
        <b class="text-amber-400 font-bold text-base">★ {{ stats.avg_score ?? '—' }}</b>
      </div>
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
