<!-- components/MovieFiltersSidebar.vue -->
<template>
  <component
    :is="flat ? 'div' : 'aside'"
    :class="[
      'text-white w-full space-y-6',
      flat ? 'p-0 bg-transparent border-0 shadow-none' : 'bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-md shadow-xl'
    ]"
  >
    <div>
      <h2 class="text-lg font-bold tracking-tight text-white mb-1">Filtri</h2>
      <p class="text-xs text-gray-400">
        Affina la tua libreria per titolo, stato e tipo.
      </p>
    </div>

    <div class="space-y-4">
      <!-- Search -->
      <div>
        <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
          Cerca
        </label>
        <div class="relative">
          <span class="absolute inset-y-0 left-0 flex items-center pl-3.5 pointer-events-none text-gray-500">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </span>
          <input
            v-model="qProxy"
            placeholder="Titolo o nota…"
            class="w-full bg-white/5 border border-white/10 text-white text-sm rounded-xl py-2.5 pl-10 pr-3 focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all placeholder-gray-500 outline-none"
          />
        </div>
      </div>

      <!-- Tipo -->
      <div>
        <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
          Tipo
        </label>
        <div class="relative">
          <select
            v-model="kindProxy"
            class="appearance-none bg-none w-full bg-white/5 border border-white/10 text-white text-sm rounded-xl py-2.5 pl-3 pr-10 focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all [&>option]:bg-slate-950 [&>option]:text-white cursor-pointer outline-none"
          >
            <option value="">Tutti</option>
            <option value="movie">Solo film</option>
            <option value="tv">Solo serie</option>
          </select>
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3.5 text-gray-400">
            <svg class="w-4 h-4 stroke-current" fill="none" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Stato -->
      <div>
        <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
          Stato
        </label>
        <div class="relative">
          <select
            v-model="statusProxy"
            class="appearance-none bg-none w-full bg-white/5 border border-white/10 text-white text-sm rounded-xl py-2.5 pl-3 pr-10 focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all [&>option]:bg-slate-950 [&>option]:text-white cursor-pointer outline-none"
          >
            <option value="">Tutti</option>
            <option value="to_watch">Da vedere</option>
            <option value="watched">Visto</option>
            <option value="upcoming">In uscita</option>
            <option value="watching">In visione</option>
          </select>
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3.5 text-gray-400">
            <svg class="w-4 h-4 stroke-current" fill="none" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Ordinamento -->
      <div>
        <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
          Ordina per
        </label>
        <div class="relative">
          <select
            v-model="sortByProxy"
            class="appearance-none bg-none w-full bg-white/5 border border-white/10 text-white text-sm rounded-xl py-2.5 pl-3 pr-10 focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all [&>option]:bg-slate-950 [&>option]:text-white cursor-pointer outline-none"
          >
            <option value="created_at_desc">Recenti</option>
            <option value="title_asc">Titolo A→Z</option>
            <option value="score_desc">Score alto</option>
          </select>
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3.5 text-gray-400">
            <svg class="w-4 h-4 stroke-current" fill="none" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Reset -->
    <div class="flex justify-between items-center pt-2">
      <button
        type="button"
        class="inline-flex items-center gap-1.5 text-xs text-gray-400 hover:text-white transition-colors"
        @click="$emit('reset')"
      >
        <svg
          class="w-4 h-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
          />
        </svg>
        <span>Reset filtri</span>
      </button>
    </div>

    <!-- Top Registi -->
    <div v-if="stats?.stats_advanced?.directors?.length" class="border-t border-white/10 pt-4">
      <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">I tuoi registi preferiti</h3>
      <div class="flex flex-wrap gap-2">
        <NuxtLink
          v-for="dir in stats.stats_advanced.directors"
          :key="dir.name"
          :to="{ path: '/dashboard', query: { director: dir.name } }"
          class="px-2.5 py-1 bg-white/5 hover:bg-purple-500/10 text-gray-300 hover:text-purple-300 border border-white/5 hover:border-purple-500/30 transition rounded-lg text-xs font-medium block w-max"
        >
          {{ dir.name }} <span class="text-gray-500">({{ dir.count }})</span>
        </NuxtLink>
      </div>
    </div>

    <!-- Top Attori -->
    <div v-if="stats?.stats_advanced?.actors?.length" class="space-y-3">
      <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">I tuoi attori preferiti</h3>
      <div class="flex flex-wrap gap-2">
        <NuxtLink
          v-for="actor in stats.stats_advanced.actors"
          :key="actor.name"
          :to="{ path: '/dashboard', query: { cast: actor.name } }"
          class="px-2.5 py-1 bg-white/5 hover:bg-purple-500/10 text-gray-300 hover:text-purple-300 border border-white/5 hover:border-purple-500/30 transition rounded-lg text-xs font-medium block w-max"
        >
          {{ actor.name }} <span class="text-gray-500">({{ actor.count }})</span>
        </NuxtLink>
      </div>
    </div>

    <!-- 📊 STATISTICHE SOTTO I FILTRI, NELLA STESSA CARD -->
    <div class="border-t border-white/10 pt-4">
      <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Statistiche</h3>
      <p class="text-[10px] text-gray-500 mb-4">Panoramica rapida della tua libreria</p>
      <DashboardStats v-if="stats" :stats="stats" />
    </div>
  </component>
</template>

<script setup>
import DashboardStats from "@/components/DashboardStats.vue"

const props = defineProps({
  q: { type: String, default: '' },
  status: { type: String, default: '' },
  kind: { type: String, default: '' },
  sortBy: { type: String, default: 'created_at_desc' },
  stats: { type: Object, default: null },
  flat: { type: Boolean, default: false }
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
