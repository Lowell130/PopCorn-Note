<!-- components/MovieFiltersSidebar.vue -->
<template>
<aside class="bg-white p-4 rounded-lg top-6 self-start text-gray-800 shadow-sm dark:border-gray-700 dark:bg-gray-800 w-full">
    <h2 class="text-lg font-semibold mb-1">Filtri</h2>
    <p class="text-xs text-gray-500 mb-4">
      Affina la tua libreria per titolo, stato e tipo.
    </p>

    <div class="space-y-3">
      <!-- Search -->
      <div>
        <label class="block text-xs font-medium text-gray-500 mb-1">
          Cerca
        </label>
        <input
          v-model="qProxy"
          placeholder="Titolo o nota…"
          class="w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5"
        />
      </div>

      <!-- Tipo -->
      <div>
        <label class="block text-xs font-medium text-gray-500 mb-1">
          Tipo
        </label>
        <select
          v-model="kindProxy"
          class="w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg p-2.5"
        >
          <option value="">Tutti</option>
          <option value="movie">Solo film</option>
          <option value="tv">Solo serie</option>
        </select>
      </div>

      <!-- Stato -->
      <div>
        <label class="block text-xs font-medium text-gray-500 mb-1">
          Stato
        </label>
        <select
          v-model="statusProxy"
          class="w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg p-2.5"
        >
          <option value="">Tutti</option>
          <option value="to_watch">Da vedere</option>
          <option value="watched">Visto</option>
          <option value="upcoming">In uscita</option>
          <option value="watching">In visione</option>
        </select>
      </div>

      <!-- Ordinamento -->
      <div>
        <label class="block text-xs font-medium text-gray-500 mb-1">
          Ordina per
        </label>
        <select
          v-model="sortByProxy"
          class="w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg p-2.5"
        >
          <option value="created_at_desc">Recenti</option>
          <option value="title_asc">Titolo A→Z</option>
          <option value="score_desc">Score alto</option>
        </select>
      </div>
    </div>

    <!-- Reset -->
    <div class="mt-5 flex justify-between items-center">
      <button
        type="button"
        class="inline-flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700"
        @click="$emit('reset')"
      >
        <svg
          class="w-4 h-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M17.651 7.65a7.131 7.131 0 0 0-12.68 3.15M18.001 4v4h-4m-7.652 8.35a7.13 7.13 0 0 0 12.68-3.15M6 20v-4h4"
          />
        </svg>
        Reset filtri
      </button>
    </div>

    <!-- Top Registi -->
    <div v-if="stats?.stats_advanced?.directors?.length" class="mt-6 border-t dark:border-gray-700 pt-4">
      <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">I tuoi registi preferiti</h3>
      <div class="flex flex-wrap gap-2">
        <NuxtLink
          v-for="dir in stats.stats_advanced.directors"
          :key="dir.name"
          :to="{ path: '/dashboard', query: { director: dir.name } }"
          class="px-2 py-1 bg-gray-100 dark:bg-gray-700 hover:bg-blue-100 dark:hover:bg-blue-900/40 transition rounded-md text-xs text-gray-700 dark:text-gray-300 hover:text-blue-700 dark:hover:text-blue-300 border border-gray-200 dark:border-gray-600 block w-max"
        >
          {{ dir.name }} <span class="text-gray-400 dark:text-gray-500">({{ dir.count }})</span>
        </NuxtLink>
      </div>
    </div>

    <!-- Top Attori -->
    <div v-if="stats?.stats_advanced?.actors?.length" class="mt-4">
      <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">I tuoi attori preferiti</h3>
      <div class="flex flex-wrap gap-2">
        <NuxtLink
          v-for="actor in stats.stats_advanced.actors"
          :key="actor.name"
          :to="{ path: '/dashboard', query: { cast: actor.name } }"
          class="px-2 py-1 bg-gray-100 dark:bg-gray-700 hover:bg-purple-100 dark:hover:bg-purple-900/40 transition rounded-md text-xs text-gray-700 dark:text-gray-300 hover:text-purple-700 dark:hover:text-purple-300 border border-gray-200 dark:border-gray-600 block w-max"
        >
          {{ actor.name }} <span class="text-gray-400 dark:text-gray-500">({{ actor.count }})</span>
        </NuxtLink>
      </div>
    </div>

      <!-- 📊 STATISTICHE SOTTO I FILTRI, NELLA STESSA CARD -->
     <h2 class="text-lg font-semibold mb-1 mt-6 border-t dark:border-gray-700 pt-4">Statistiche</h2>
     <p class="text-xs text-gray-500 mb-4 pb-2">Visualizza le statistiche della libreria </p>
    <DashboardStats v-if="stats" :stats="stats" />
  </aside>
</template>

<script setup>
const props = defineProps({
  q: { type: String, default: '' },
  status: { type: String, default: '' },
  kind: { type: String, default: '' },
  sortBy: { type: String, default: 'created_at_desc' },
  stats: { type: Object, default: null }   // 👈 NUOVO
})

const emit = defineEmits([
  'update:q',
  'update:status',
  'update:kind',
  'update:sortBy',
  'reset'
])

// Proxy per usare v-model direttamente nel child
const qProxy = computed({
  get: () => props.q,
  set: (val) => emit('update:q', val)
})

const statusProxy = computed({
  get: () => props.status,
  set: (val) => emit('update:status', val)
})

const kindProxy = computed({
  get: () => props.kind,
  set: (val) => emit('update:kind', val)
})

const sortByProxy = computed({
  get: () => props.sortBy,
  set: (val) => emit('update:sortBy', val)
})
</script>
