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

            <td class="px-6 py-4">
              <button
                class="inline-flex items-center gap-2 px-3 py-1.5 text-white bg-red-600 hover:bg-red-700 rounded disabled:opacity-60"
                :disabled="deletingId === u.id || u.id === me?.id"
                @click="confirmDelete(u)"
                title="Delete user"
              >
                <svg v-if="deletingId !== u.id" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M9 3h6a1 1 0 0 1 1 1v1h4v2h-1l-1 13a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 7H4V5h4V4a1 1 0 0 1 1-1Zm2 0v1h2V3h-2ZM8 9h2v10H8V9Zm4 0h2v10h-2V9Z"/></svg>
                <svg v-else class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4A4 4 0 008 12H4z"/>
                </svg>
                Delete
              </button>
              <!-- <div v-if="u.id === me?.id" class="text-xs text-gray-400 mt-1">You</div> -->
            </td>
          </tr>
        </tbody>
      </table>
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
</script>
