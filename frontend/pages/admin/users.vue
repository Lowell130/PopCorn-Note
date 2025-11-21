<!-- pages/admin/users.vue -->
<template>
  <div>
    <!-- Header + pulsanti TMDb -->
    <div class="mb-6 flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-2xl font-semibold text-black">User Management</h1>
        <p class="text-sm text-gray-500">
          Gestisci utenti e avvia strumenti di manutenzione TMDb.
        </p>
      </div>

      <!-- Box strumenti TMDb -->
      <div class="flex flex-col items-end gap-2 w-full sm:w-auto">
        <!-- Pulsante principale: aggiorna TUTTI -->
        <button
          @click="runFullBackfillTmdbVotes"
          class="inline-flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium rounded-lg text-white bg-purple-700 hover:bg-purple-800 focus:outline-none focus:ring-4 focus:ring-purple-300 disabled:opacity-60 w-full sm:w-auto"
          :disabled="backfillRunning"
        >
          <svg
    v-if="!backfillRunning"
    class="w-5 h-5 text-white"
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
            {{ backfillRunning ? 'Aggiorno tutti i voti TMDb…' : 'Aggiorna tutti i voti TMDb' }}
          </span>
        </button>

        <!-- Barra progresso (indeterminata) -->
        <div v-if="backfillRunning" class="w-full sm:w-64">
          <div class="h-1.5 w-full bg-purple-100 rounded-full overflow-hidden">
            <div class="h-full w-1/2 bg-purple-500 animate-pulse"></div>
          </div>
        </div>

        <!-- Messaggi -->
        <div class="text-right w-full sm:w-64 space-y-0.5">
          <p v-if="backfillStats.totalUpdated > 0" class="text-xs text-emerald-700">
            Aggiornati finora: {{ backfillStats.totalUpdated }} elementi TMDb
            <span v-if="backfillStats.batches > 1">
              ({{ backfillStats.batches }} batch)
            </span>
          </p>
          <p v-if="typeof backfillStats.lastUpdated === 'number'" class="text-xs text-gray-500">
            Ultimo batch: {{ backfillStats.lastUpdated }} aggiornati
            <span v-if="typeof backfillStats.lastRemaining === 'number'">
              – rimanenti stimati: {{ backfillStats.lastRemaining }}
            </span>
          </p>
          <p v-if="backfillMessage" class="text-xs text-emerald-700">
            {{ backfillMessage }}
          </p>
          <p v-if="backfillError" class="text-xs text-red-600">
            {{ backfillError }}
          </p>
        </div>
      </div>
    </div>
    <!-- <h1 class="text-2xl font-semibold text-black mb-6">User Management</h1> -->


    <div v-if="loading" class="opacity-70">Loading…</div>
    <div v-else-if="error" class="text-red-600">Error: {{ error }}</div>

    <div v-else class="relative overflow-x-auto shadow rounded-xl">
      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
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
            class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200"
          >
            <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
              {{ u.username || '—' }}
            </th>
            <td class="px-6 py-4">{{ u.email }}</td>
            <td class="px-6 py-4">
              <span :class="u.is_admin ? 'text-emerald-700 font-semibold' : 'text-gray-500'">
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

    <!-- Modal Edit -->
    <div
      v-if="editingUser"
      class="fixed inset-0 z-20 flex items-center justify-center bg-black/50 p-4"
      @click.self="closeEdit"
    >
      <div class="w-full max-w-lg bg-white text-black rounded-xl shadow p-5">
        <h2 class="text-lg font-semibold mb-4">Edit user</h2>

        <div class="space-y-3">
          <div>
            <label class="block text-sm mb-1">Email</label>
            <input v-model="form.email" type="email" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" />
          </div>
          <div>
            <label class="block text-sm mb-1">Username</label>
            <input v-model="form.username" type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" />
          </div>
          <div>
            <label class="block text-sm mb-1">Password (leave blank to keep)</label>
            <input v-model="form.password" type="password" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" />
          </div>
          <div class="flex items-center gap-2">
            <input id="is_admin" v-model="form.is_admin" type="checkbox" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600" />
            <label for="is_admin" class="text-sm">Administrator</label>
          </div>

          <div v-if="editError" class="text-sm text-red-600">{{ editError }}</div>
        </div>

        <div class="mt-5 flex justify-end gap-2">
          <button
          class="text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700"
            @click="closeEdit"
            :disabled="savingId === editingUser?.id"
          >
            Cancel
          </button>
          <button
           class="focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800"
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

onMounted(fetchUsers)

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

// 🔁 BACKFILL IN LOOP FINO A ESAURIMENTO
async function runFullBackfillTmdbVotes() {
  if (backfillRunning.value) return

  backfillRunning.value = true
  backfillMessage.value = ''
  backfillError.value = ''
  backfillStats.totalUpdated = 0
  backfillStats.batches = 0
  backfillStats.lastUpdated = null
  backfillStats.lastRemaining = null

  const batchSize = 100
  const maxBatches = 100  // sicurezza per evitare loop infinito

  try {
    for (let i = 0; i < maxBatches; i++) {
      const res = await apiFetch('/admin/tmdb-tools/backfill-tmdb-votes', {
        method: 'POST',
        query: { limit: batchSize, force: false },
      })

      const updated = res?.updated ?? 0
      const remaining = res?.remaining

      backfillStats.batches += 1
      backfillStats.totalUpdated += updated
      backfillStats.lastUpdated = updated
      backfillStats.lastRemaining = typeof remaining === 'number' ? remaining : null

      // se il batch non ha aggiornato nulla, fermati
      if (!updated || updated === 0) break

      // se remaining è 0, fermati
      if (typeof remaining === 'number' && remaining <= 0) break
    }

    if (backfillStats.totalUpdated === 0) {
      backfillMessage.value = 'Nessun elemento TMDb da aggiornare.'
    } else {
      backfillMessage.value = `Backfill completato. Aggiornati ${backfillStats.totalUpdated} elementi in ${backfillStats.batches} batch.`
    }
  } catch (e) {
    backfillError.value =
      e?.response?._data?.detail ||
      e?.message ||
      'Errore durante aggiornamento voti TMDb'
  } finally {
    backfillRunning.value = false
  }
}
</script>

