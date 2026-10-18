<!-- pages/admin/users.vue -->
<template>
  <div class="space-y-8 max-w-7xl mx-auto px-4 py-6">
    <!-- Header -->
    <div class="border-b border-white/10 pb-6">
      <h1 class="text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
        Pannello di Controllo Admin
      </h1>
      <p class="text-sm text-gray-400 mt-1">
        Gestisci gli utenti registrati e sincronizza i dati dei film con TMDb.
      </p>
    </div>

    <!-- Admin Tools Grid -->
    <div class="grid grid-cols-1 gap-6">
      
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


    </div>

    <!-- User Management Table Section -->
    <div class="space-y-4 pt-4">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold text-white tracking-tight">
          Gestione Utenti Registrati
        </h2>
        <div class="flex items-center gap-2">
          <span class="text-xs bg-slate-800 text-slate-300 border border-white/10 rounded-full px-3 py-1 font-semibold">
            Totale Utenti: {{ users.length }}
          </span>
          <button
            @click="openCreate"
            class="px-3 py-1.5 text-xs font-semibold rounded-xl text-purple-200 bg-purple-500/20 border border-purple-500/40 hover:bg-purple-500/30 transition"
          >
            + Nuovo utente
          </button>
        </div>
      </div>

      <div v-if="loading" class="opacity-70 text-center py-10">Caricamento in corso…</div>
      <div v-else-if="error" class="text-red-400 text-center py-10 bg-red-500/10 border border-red-500/20 rounded-2xl">
        Errore: {{ error }}
      </div>

      <div v-else class="relative overflow-x-auto shadow-xl border border-white/10 rounded-3xl custom-scrollbar pb-2">
      <table class="w-full text-sm text-left text-gray-300">
        <thead class="text-xs text-gray-400 uppercase bg-white/5 border-b border-white/10">
          <tr>
            <th class="px-6 py-3">Username</th>
            <th class="px-6 py-3">Email</th>
            <th class="px-6 py-3">Admin</th>
            <th class="px-6 py-3">Total</th>
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
            </th>
            <td class="px-6 py-4">{{ u.email }}</td>
            <td class="px-6 py-4">
              <span :class="u.is_admin ? 'text-emerald-400 font-semibold' : 'text-gray-500'">
                {{ u.is_admin ? 'Yes' : 'No' }}
              </span>
            </td>
            <td class="px-6 py-4">{{ u.stats?.total ?? 0 }}</td>
            <td class="px-6 py-4">{{ u.stats?.avg_score ?? '—' }}</td>

       <td class="px-6 py-4 space-x-2 flex items-center justify-start">
  <!-- Edit -->
  <button
    class="p-2 rounded-full text-gray-400 hover:text-gray-300 hover:bg-white/5 transition-all disabled:opacity-50"
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
    class="p-2 rounded-full text-gray-400 hover:text-red-400 hover:bg-white/5 transition-all disabled:opacity-50"
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

    <!-- Modal Nuovo Utente -->
    <div
      v-if="creating"
      class="fixed inset-0 z-20 flex items-center justify-center bg-black/50 p-4"
      @click.self="closeCreate"
    >
      <form @submit.prevent="saveCreate" class="w-full max-w-lg bg-slate-900 border border-white/10 text-white rounded-2xl shadow-2xl p-6 backdrop-blur-md">
        <h2 class="text-lg font-bold mb-1">Nuovo utente</h2>
        <p class="text-xs text-gray-400 mb-4">Le registrazioni pubbliche sono chiuse: gli account si creano solo da qui.</p>

        <div class="space-y-3">
          <div>
            <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Email</label>
            <input v-model="createForm.email" type="email" required autocomplete="off" class="w-full bg-white/5 border border-white/10 text-white placeholder-gray-500 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Username</label>
            <input v-model="createForm.username" type="text" required minlength="3" maxlength="30" autocomplete="off" class="w-full bg-white/5 border border-white/10 text-white placeholder-gray-500 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Password</label>
            <input v-model="createForm.password" type="password" required minlength="8" autocomplete="new-password" class="w-full bg-white/5 border border-white/10 text-white placeholder-gray-500 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition" />
            <p class="text-[11px] text-gray-500 mt-1">Almeno 8 caratteri, con lettere e numeri o simboli.</p>
          </div>
          <div class="flex items-center gap-2">
            <input id="create_is_admin" v-model="createForm.is_admin" type="checkbox" class="w-4 h-4 text-purple-600 bg-white/5 border border-white/10 rounded focus:ring-purple-500 focus:ring-2" />
            <label for="create_is_admin" class="text-sm font-medium">Administrator</label>
          </div>

          <div v-if="createError" class="text-sm text-red-400 font-semibold">{{ createError }}</div>
        </div>

        <div class="mt-6 flex justify-end gap-2 border-t border-white/5 pt-4">
          <button type="button" class="px-4 py-2 text-sm font-semibold rounded-xl border border-white/10 text-gray-300 hover:bg-white/5 transition" @click="closeCreate" :disabled="creatingBusy">
            Annulla
          </button>
          <button type="submit" class="px-4 py-2 text-sm font-semibold rounded-xl text-green-300 bg-green-500/10 border border-green-500/20 hover:bg-green-500/20 transition disabled:opacity-50" :disabled="creatingBusy">
            {{ creatingBusy ? 'Creazione…' : 'Crea utente' }}
          </button>
        </div>
      </form>
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

// 🔹 Creazione nuovo utente (registrazioni pubbliche chiuse)
const creating = ref(false)
const creatingBusy = ref(false)
const createError = ref('')
const createForm = reactive({ email: '', username: '', password: '', is_admin: false })

function openCreate() {
  Object.assign(createForm, { email: '', username: '', password: '', is_admin: false })
  createError.value = ''
  creating.value = true
}

function closeCreate() {
  creating.value = false
  createForm.password = ''
}

async function saveCreate() {
  if (creatingBusy.value) return
  creatingBusy.value = true
  createError.value = ''
  try {
    const created = await apiFetch('/admin/users', { method: 'POST', body: { ...createForm } })
    users.value = [...users.value, created]
    closeCreate()
  } catch (e) {
    const d = e?.data?.detail
    createError.value = typeof d === 'string' ? d : 'Controlla i dati inseriti (email valida, username e password).'
  } finally {
    creatingBusy.value = false
  }
}

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
    if (form.password && form.password.trim().length >= 8) payload.password = form.password
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

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 9999px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(147, 51, 234, 0.5);
  border-radius: 9999px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(147, 51, 234, 0.8);
}
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: rgba(147, 51, 234, 0.5) rgba(255, 255, 255, 0.03);
}
</style>

