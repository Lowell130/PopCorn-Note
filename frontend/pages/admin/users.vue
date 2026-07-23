<!-- pages/admin/users.vue -->
<template>
  <div class="space-y-8 max-w-7xl mx-auto px-4 py-6">
    <!-- Header -->
    <div class="border-b border-white/10 pb-6">
      <h1 class="text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
        Pannello di Controllo Admin
      </h1>
      <p class="text-sm text-gray-400 mt-1">
        Gestisci gli utenti registrati, configura l'assistente AI e sincronizza i dati dei film con TMDb.
      </p>
    </div>

    <!-- Admin Tools Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- CARD 1: Sincronizzazione TMDb -->
      <div class="bg-slate-900/60 border border-white/10 rounded-3xl p-6 backdrop-blur-md flex flex-col justify-between gap-4">
        <div class="space-y-2">
          <h2 class="text-lg font-bold text-white flex items-center gap-2">
            <span class="p-1.5 rounded-xl bg-purple-500/20 text-purple-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
              </svg>
            </span>
            Sincronizzazione TMDb
          </h2>
          <p class="text-xs text-gray-400 leading-relaxed">
            Aggiorna i voti, le durate, le descrizioni e le altre info dei film della collezione allineandoli a TMDb.
          </p>
        </div>

        <div class="space-y-4">
          <!-- Bottone di avvio -->
          <button
            @click="runFullBackfillTmdbVotes"
            class="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 text-xs font-semibold rounded-xl text-white bg-purple-700 hover:bg-purple-600 focus:outline-none transition disabled:opacity-60 cursor-pointer"
            :disabled="backfillRunning"
          >
            <svg
              v-if="!backfillRunning"
              class="w-4 h-4 text-white"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17.651 7.65a7.131 7.131 0 0 0-12.68 3.15M18.001 4v4h-4m-7.652 8.35a7.13 7.13 0 0 0 12.68-3.15M6 20v-4h4"
              />
            </svg>
            <svg
              v-else
              class="animate-spin h-4 w-4"
              viewBox="0 0 24 24"
              fill="none"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              />
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v4A4 4 0 008 12H4z"
              />
            </svg>

            <span>
              {{ backfillRunning ? 'Sincronizzazione dati TMDb in corso…' : 'Sincronizza Voti e Info TMDb' }}
            </span>
          </button>

          <!-- Barra progresso -->
          <div v-if="backfillRunning" class="w-full">
            <div class="h-1.5 w-full bg-purple-100/10 rounded-full overflow-hidden">
              <div class="h-full w-1/2 bg-purple-500 animate-pulse"></div>
            </div>
          </div>

          <!-- Log Messaggi -->
          <div class="space-y-1">
            <p v-if="backfillStats.totalUpdated > 0" class="text-[11px] text-emerald-400">
              ✔ Aggiornati finora: <span class="font-bold text-white">{{ backfillStats.totalUpdated }}</span> elementi
              <span v-if="backfillStats.batches > 1">({{ backfillStats.batches }} batch)</span>
            </p>
            <p v-if="typeof backfillStats.lastUpdated === 'number'" class="text-[11px] text-gray-400">
              Ultimo batch: {{ backfillStats.lastUpdated }} aggiornati
              <span v-if="typeof backfillStats.lastRemaining === 'number'" class="text-purple-300 block mt-0.5">
                • Rimanenti da sincronizzare: <span class="font-bold text-white">{{ backfillStats.lastRemaining }}</span>
              </span>
            </p>
            <p v-if="backfillMessage" class="text-[11px] text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-2">
              {{ backfillMessage }}
            </p>
            <p v-if="backfillError" class="text-[11px] text-red-400 bg-red-500/10 border border-red-500/20 rounded-xl p-2">
              {{ backfillError }}
            </p>
          </div>
        </div>
      </div>

      <!-- CARD 2: Community Simulator -->
      <div class="bg-slate-900/60 border border-white/10 rounded-3xl p-6 backdrop-blur-md flex flex-col justify-between gap-4">
        <div class="space-y-2">
          <h2 class="text-lg font-bold text-white flex items-center gap-2">
            <span class="p-1.5 rounded-xl bg-indigo-500/20 text-indigo-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </span>
            Community Simulator
          </h2>
          <p class="text-xs text-gray-400 leading-relaxed">
            Popola la community con utenti e attività fittizie per testare il feed e le funzioni social.
          </p>
        </div>

        <div class="space-y-4">
          <!-- Stats utenti -->
          <div class="flex gap-3">
            <div class="bg-white/5 border border-white/5 rounded-2xl px-4 py-2.5 flex-1">
              <span class="block text-[10px] font-semibold text-gray-500 uppercase">Fake Users</span>
              <span class="text-xl font-extrabold text-indigo-400">{{ fakeUsersCount }}</span>
            </div>
            <div class="bg-white/5 border border-white/5 rounded-2xl px-4 py-2.5 flex-1">
              <span class="block text-[10px] font-semibold text-gray-500 uppercase">Real Users</span>
              <span class="text-xl font-extrabold text-emerald-400">{{ realUsersCount }}</span>
            </div>
          </div>

          <!-- Slider quantità -->
          <div>
            <label class="block text-[10px] font-semibold text-gray-500 uppercase tracking-wider mb-1.5">Quantità da Generare</label>
            <div class="flex items-center gap-3 bg-white/5 border border-white/10 rounded-xl px-3 py-1.5">
              <input type="range" v-model.number="fakeCount" min="1" max="50" class="w-full accent-indigo-500 bg-white/10 rounded-lg appearance-none cursor-pointer" />
              <span class="text-sm font-bold text-white w-6 text-right">{{ fakeCount }}</span>
            </div>
          </div>

          <!-- Pulsanti azioni -->
          <div class="space-y-2">
            <div class="flex gap-2">
              <button
                @click="generateFakeUsers"
                class="flex-1 inline-flex items-center justify-center gap-2 px-4 py-2.5 text-xs font-semibold rounded-xl text-white bg-indigo-600 hover:bg-indigo-500 transition disabled:opacity-50 cursor-pointer"
                :disabled="generatorRunning"
              >
                <svg v-if="generatorRunning" class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4A4 4 0 008 12H4z"></path>
                </svg>
                <span>{{ generatorRunning ? 'Generazione…' : 'Genera Utenti' }}</span>
              </button>

              <button
                @click="handleDeleteFake"
                class="inline-flex items-center justify-center gap-2 px-3 py-2.5 text-xs font-semibold rounded-xl transition cursor-pointer"
                :class="deleteConfirmedOnce ? 'bg-red-700 hover:bg-red-600 text-white animate-pulse' : 'bg-red-500/10 border border-red-500/20 text-red-400 hover:bg-red-500/20'"
                :disabled="generatorRunning"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                <span>{{ deleteConfirmedOnce ? 'Confermi?' : 'Pulisci Fake' }}</span>
              </button>
            </div>

            <!-- Messaggi simulator -->
            <div v-if="generatorMessage" class="text-[11px] text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-2">
              {{ generatorMessage }}
            </div>
            <div v-if="generatorError" class="text-[11px] text-red-400 bg-red-500/10 border border-red-500/20 rounded-xl p-2">
              {{ generatorError }}
            </div>
          </div>
        </div>
      </div>

      <!-- CARD 3: PopcornBot AI -->
      <div class="bg-slate-900/60 border border-white/10 rounded-3xl p-6 backdrop-blur-md flex flex-col justify-between gap-4">
        <div class="space-y-2">
          <h2 class="text-lg font-bold text-white flex items-center gap-2">
            <span class="p-1.5 rounded-xl bg-slate-500/20 text-slate-300">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </span>
            Assistente AI PopcornBot
          </h2>
          <p class="text-xs text-gray-400 leading-relaxed">
            Configura il comportamento, la personalità e le impostazioni dei suggerimenti dell'assistente AI.
          </p>
        </div>

        <div class="space-y-4">
          <div class="bg-white/5 border border-white/5 rounded-2xl p-4 text-xs text-gray-400 space-y-2">
            <p>• Personalità e tono personalizzati</p>
            <p>• Supporto per suggerimenti basati sui tuoi gusti</p>
            <p>• Risposte generate in tempo reale tramite LLM</p>
          </div>

          <NuxtLink
            to="/admin/settings"
            class="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 text-xs font-semibold rounded-xl text-white bg-slate-800 hover:bg-slate-700 border border-white/10 transition shadow-md cursor-pointer"
          >
            <span>🍿 Impostazioni Bot AI</span>
          </NuxtLink>
        </div>
      </div>

    </div>

    <!-- User Management Table Section -->
    <div class="space-y-4 pt-4">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold text-white tracking-tight">
          Gestione Utenti Registrati
        </h2>
        <span class="text-xs bg-slate-800 text-slate-300 border border-white/10 rounded-full px-3 py-1 font-semibold">
          Totale Utenti: {{ users.length }}
        </span>
      </div>

      <div v-if="loading" class="opacity-70 text-center py-10">Caricamento in corso…</div>
      <div v-else-if="error" class="text-red-400 text-center py-10 bg-red-500/10 border border-red-500/20 rounded-2xl">
        Errore: {{ error }}
      </div>

      <div v-else class="relative overflow-x-auto shadow-xl border border-white/10 rounded-3xl">
      <table class="w-full text-sm text-left text-gray-300">
        <thead class="text-xs text-gray-400 uppercase bg-white/5 border-b border-white/10">
          <tr>
            <th class="px-6 py-3">Username</th>
            <th class="px-6 py-3">Email</th>
            <th class="px-6 py-3">Admin</th>
            <th class="px-6 py-3">Total</th>
            <th class="px-6 py-3">Watching</th>
            <th class="px-6 py-3">To watch</th>
            <th class="px-6 py-3">Watched</th>
            <th class="px-6 py-3">Upcoming</th>
            <th class="px-6 py-3">Avg Score</th>
            <th class="px-6 py-3">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="u in users"
            :key="u.id"
            class="bg-transparent border-b border-white/5 text-gray-300 hover:bg-white/5 transition-colors"
          >
            <th scope="row" class="px-6 py-4 font-bold text-white whitespace-nowrap flex items-center gap-2">
              <span>{{ u.username || '—' }}</span>
              <span v-if="u.is_fake" class="text-[9px] bg-indigo-500/20 text-indigo-300 px-1.5 py-0.5 rounded border border-indigo-500/30 font-bold select-none uppercase tracking-wider">Fake</span>
            </th>
            <td class="px-6 py-4">{{ u.email }}</td>
            <td class="px-6 py-4">
              <span :class="u.is_admin ? 'text-emerald-400 font-semibold' : 'text-gray-500'">
                {{ u.is_admin ? 'Yes' : 'No' }}
              </span>
            </td>
            <td class="px-6 py-4">{{ u.stats?.total ?? 0 }}</td>
            <td class="px-6 py-4">{{ u.stats?.watching ?? 0 }}</td>
            <td class="px-6 py-4">{{ u.stats?.to_watch ?? 0 }}</td>
            <td class="px-6 py-4">{{ u.stats?.watched ?? 0 }}</td>
            <td class="px-6 py-4">{{ u.stats?.upcoming ?? 0 }}</td>
            <td class="px-6 py-4">{{ u.stats?.avg_score ?? '—' }}</td>

       <td class="px-6 py-4 space-x-2">
  <!-- Edit -->
  <button
    class="p-2 rounded-full text-gray-400 hover:text-gray-600 disabled:opacity-50"
    :disabled="savingId === u.id"
    @click="openEdit(u)"
    title="Edit user"
  >
    <svg v-if="savingId !== u.id" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536M9 13l6.232-6.232a2 2 0 112.828 2.828L11.828 15.828a2 2 0 01-1.414.586H9v-1.414a2 2 0 01.586-1.414z" />
    </svg>
    <svg v-else class="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4A4 4 0 008 12H4z"/>
    </svg>
  </button>

  <!-- Delete -->
  <button
    class="p-2 rounded-full text-gray-400 hover:text-gray-600 disabled:opacity-50"
    :disabled="deletingId === u.id || u.id === me?.id"
    @click="confirmDelete(u)"
    title="Delete user"
  >
    <svg v-if="deletingId !== u.id" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
    </svg>
    <svg v-else class="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4A4 4 0 008 12H4z"/>
    </svg>
  </button>
</td>

          </tr>
        </tbody>
      </table>
    </div>
  </div>

    <!-- Modal Edit -->
    <div
      v-if="editingUser"
      class="fixed inset-0 z-20 flex items-center justify-center bg-black/50 p-4"
      @click.self="closeEdit"
    >
      <div class="w-full max-w-lg bg-slate-900 border border-white/10 text-white rounded-2xl shadow-2xl p-6 backdrop-blur-md">
        <h2 class="text-lg font-bold mb-4">Edit user</h2>

        <div class="space-y-3">
          <div>
            <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Email</label>
            <input v-model="form.email" type="email" class="w-full bg-white/5 border border-white/10 text-white placeholder-gray-500 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Username</label>
            <input v-model="form.username" type="text" class="w-full bg-white/5 border border-white/10 text-white placeholder-gray-500 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Password (leave blank to keep)</label>
            <input v-model="form.password" type="password" class="w-full bg-white/5 border border-white/10 text-white placeholder-gray-500 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition" />
          </div>
          <div class="flex items-center gap-2">
            <input id="is_admin" v-model="form.is_admin" type="checkbox" class="w-4 h-4 text-purple-600 bg-white/5 border border-white/10 rounded focus:ring-purple-500 focus:ring-2" />
            <label for="is_admin" class="text-sm font-medium">Administrator</label>
          </div>

          <div v-if="editError" class="text-sm text-red-400 font-semibold">{{ editError }}</div>
        </div>

        <div class="mt-6 flex justify-end gap-2 border-t border-white/5 pt-4">
          <button
            class="px-4 py-2 text-sm font-semibold rounded-xl border border-white/10 text-gray-300 hover:bg-white/5 transition"
            @click="closeEdit"
            :disabled="savingId === editingUser?.id"
          >
            Cancel
          </button>
          <button
            class="px-4 py-2 text-sm font-semibold rounded-xl text-green-300 bg-green-500/10 border border-green-500/20 hover:bg-green-500/20 transition disabled:opacity-50"
            @click="saveEdit"
            :disabled="savingId === editingUser?.id"
          >
            <span v-if="savingId !== editingUser?.id">Save</span>
            <span v-else>Saving…</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
definePageMeta({ middleware: ['admin-only'], layout: 'wide' })

const { apiFetch } = useApi()
const { user: me } = useAuth()

const users = ref([])
const loading = ref(false)
const error = ref('')
const deletingId = ref(null)

const editingUser = ref(null)
const savingId = ref(null)
const editError = ref('')

// form edit
const form = reactive({
  email: '',
  username: '',
  password: '',
  is_admin: false,
})

// 🔹 Stato per backfill TMDb
const backfillRunning = ref(false)
const backfillMessage = ref('')
const backfillError = ref('')
const backfillStats = reactive({
  totalUpdated: 0,
  batches: 0,
  lastUpdated: null,
  lastRemaining: null,
})

// 🔹 Stato per simulatore community (Fake Users)
const fakeCount = ref(10)
const generatorRunning = ref(false)
const generatorMessage = ref('')
const generatorError = ref('')
const deleteConfirmedOnce = ref(false)
let deleteConfirmTimer = null

const fakeUsersCount = computed(() => users.value.filter(u => u.is_fake).length)
const realUsersCount = computed(() => users.value.filter(u => !u.is_fake).length)

async function generateFakeUsers() {
  if (generatorRunning.value) return
  generatorRunning.value = true
  generatorMessage.value = ''
  generatorError.value = ''
  try {
    const res = await apiFetch('/admin/fake-users/generate', {
      method: 'POST',
      query: { count: fakeCount.value }
    })
    generatorMessage.value = res.message || 'Utenti fake generati con successo!'
    // Ricarica la lista utenti
    await fetchUsers()
  } catch (e) {
    generatorError.value = e?.response?._data?.detail || e?.message || 'Errore durante la generazione'
  } finally {
    generatorRunning.value = false
  }
}

async function handleDeleteFake() {
  if (generatorRunning.value) return
  
  if (!deleteConfirmedOnce.value) {
    deleteConfirmedOnce.value = true
    // Resetta dopo 5 secondi
    deleteConfirmTimer = setTimeout(() => {
      deleteConfirmedOnce.value = false
    }, 5000)
    return
  }
  
  // Esegui cancellazione reale
  clearTimeout(deleteConfirmTimer)
  deleteConfirmedOnce.value = false
  generatorRunning.value = true
  generatorMessage.value = ''
  generatorError.value = ''
  
  try {
    const res = await apiFetch('/admin/fake-users', {
      method: 'DELETE'
    })
    generatorMessage.value = res.message || 'Utenti fake rimossi con successo.'
    // Ricarica la lista utenti
    await fetchUsers()
  } catch (e) {
    generatorError.value = e?.response?._data?.detail || e?.message || 'Errore durante la pulizia'
  } finally {
    generatorRunning.value = false
  }
}

onMounted(async () => {
  await fetchUsers()
  await checkBackfillStatus()
})

async function fetchUsers() {
  loading.value = true
  error.value = ''
  try {
    users.value = await apiFetch('/admin/users')
  } catch (e) {
    error.value = e?.response?._data?.detail || e?.message || 'Error'
  } finally {
    loading.value = false
  }
}

async function confirmDelete(u) {
  if (u.id === me?.value?.id) {
    alert('You cannot delete your own account.')
    return
  }
  if (!confirm(`Delete user "${u.username || u.email}"? This will also remove their movies.`)) return
  deletingId.value = u.id
  try {
    await apiFetch(`/admin/users/${u.id}`, { method: 'DELETE' })
    users.value = users.value.filter(x => x.id !== u.id)
  } catch (e) {
    alert(e?.response?._data?.detail || e?.message || 'Delete failed')
  } finally {
    deletingId.value = null
  }
}

function openEdit(u) {
  editingUser.value = u
  form.email = u.email || ''
  form.username = u.username || ''
  form.password = ''
  form.is_admin = !!u.is_admin
  editError.value = ''
}

function closeEdit() {
  editingUser.value = null
  form.email = ''
  form.username = ''
  form.password = ''
  form.is_admin = false
  editError.value = ''
}

async function saveEdit() {
  if (!editingUser.value) return
  if (editingUser.value.id === me?.value?.id && form.is_admin === false) {
    editError.value = 'You cannot remove your own admin role.'
    return
  }

  savingId.value = editingUser.value.id
  editError.value = ''
  try {
    const payload = {}
    if (form.email && form.email !== editingUser.value.email) payload.email = form.email
    if (form.username && form.username !== editingUser.value.username) payload.username = form.username
    if (form.password && form.password.trim().length >= 6) payload.password = form.password
    if (form.is_admin !== editingUser.value.is_admin) payload.is_admin = form.is_admin

    if (Object.keys(payload).length === 0) {
      closeEdit()
      return
    }

    const updated = await apiFetch(`/admin/users/${editingUser.value.id}`, {
      method: 'PUT',
      body: payload,
    })

    const idx = users.value.findIndex(x => x.id === editingUser.value.id)
    if (idx !== -1) users.value[idx] = { ...users.value[idx], ...updated }

    closeEdit()
  } catch (e) {
    editError.value = e?.response?._data?.detail || e?.message || 'Update failed'
  } finally {
    savingId.value = null
  }
}

let statusInterval = null

async function checkBackfillStatus() {
  try {
    const res = await apiFetch('/admin/tmdb-tools/backfill-status')
    
    const wasRunning = backfillRunning.value
    backfillRunning.value = res.running
    backfillStats.totalUpdated = res.total_updated
    backfillStats.lastUpdated = res.last_batch_updated
    backfillStats.lastRemaining = res.remaining
    
    if (res.error) {
      backfillError.value = res.error
    }
    
    if (wasRunning && !res.running) {
      if (res.completed) {
        backfillMessage.value = `Sincronizzazione completata! Aggiornati ${res.total_updated} elementi.`
      }
      stopPolling()
    }
    
    if (res.running) {
      startPolling()
    }
  } catch (e) {
    console.error('Errore nel recupero dello stato di sincronizzazione:', e)
  }
}

function startPolling() {
  if (statusInterval) return
  statusInterval = setInterval(checkBackfillStatus, 2000)
}

function stopPolling() {
  if (statusInterval) {
    clearInterval(statusInterval)
    statusInterval = null
  }
}

onUnmounted(() => {
  stopPolling()
})

async function runFullBackfillTmdbVotes() {
  if (backfillRunning.value) return

  backfillMessage.value = ''
  backfillError.value = ''
  backfillStats.totalUpdated = 0
  backfillStats.lastUpdated = 0
  
  try {
    const res = await apiFetch('/admin/tmdb-tools/backfill-tmdb-votes', { method: 'POST' })
    backfillRunning.value = true
    backfillStats.lastRemaining = res.state?.remaining
    startPolling()
  } catch (e) {
    backfillError.value = e?.response?._data?.detail || e?.message || 'Impossibile avviare la sincronizzazione.'
  }
}
</script>

