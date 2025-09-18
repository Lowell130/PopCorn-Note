<!-- pages/admin/users.vue -->
<template>
  <div>
    <h1 class="text-2xl font-semibold text-black mb-6">User Management</h1>

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
            <input v-model="form.email" type="email" class="w-full border rounded p-2" />
          </div>
          <div>
            <label class="block text-sm mb-1">Username</label>
            <input v-model="form.username" type="text" class="w-full border rounded p-2" />
          </div>
          <div>
            <label class="block text-sm mb-1">Password (leave blank to keep)</label>
            <input v-model="form.password" type="password" class="w-full border rounded p-2" />
          </div>
          <div class="flex items-center gap-2">
            <input id="is_admin" v-model="form.is_admin" type="checkbox" class="h-4 w-4" />
            <label for="is_admin" class="text-sm">Administrator</label>
          </div>

          <div v-if="editError" class="text-sm text-red-600">{{ editError }}</div>
        </div>

        <div class="mt-5 flex justify-end gap-2">
          <button
            class="px-4 py-2 rounded border"
            @click="closeEdit"
            :disabled="savingId === editingUser?.id"
          >
            Cancel
          </button>
          <button
            class="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-60"
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
  form.password = ''               // vuota -> non aggiorna password
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
  // blocca il self-downgrade lato FE (già gestito lato BE comunque)
  if (editingUser.value.id === me?.value?.id && form.is_admin === false) {
    editError.value = 'You cannot remove your own admin role.'
    return
  }

  savingId.value = editingUser.value.id
  editError.value = ''
  try {
    const payload = {}
    // invia solo i campi modificati/valorizzati
    if (form.email && form.email !== editingUser.value.email) payload.email = form.email
    if (form.username && form.username !== editingUser.value.username) payload.username = form.username
    if (form.password && form.password.trim().length >= 6) payload.password = form.password
    if (form.is_admin !== editingUser.value.is_admin) payload.is_admin = form.is_admin

    // se non c'è nulla da aggiornare, non chiamare l'API
    if (Object.keys(payload).length === 0) {
      closeEdit()
      return
    }

    const updated = await apiFetch(`/admin/users/${editingUser.value.id}`, {
      method: 'PUT',
      body: payload,
    })

    // aggiorna riga in memoria
    const idx = users.value.findIndex(x => x.id === editingUser.value.id)
    if (idx !== -1) users.value[idx] = { ...users.value[idx], ...updated }

    closeEdit()
  } catch (e) {
    editError.value = e?.response?._data?.detail || e?.message || 'Update failed'
  } finally {
    savingId.value = null
  }
}
</script>
