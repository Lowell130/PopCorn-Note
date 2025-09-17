<!-- pages/admin/users.vue -->
<template>
  <div>
    <h1 class="text-2xl font-semibold text-black mb-4">User Management</h1>

    <div v-if="loading" class="opacity-70">Loading…</div>
    <div v-else-if="error" class="text-red-600">Error: {{ error }}</div>

    <div v-else class="bg-white text-black rounded-xl p-4 shadow">
      <div class="overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead>
            <tr class="text-left border-b">
              <th class="py-2 pr-4">Username</th>
              <th class="py-2 pr-4">Email</th>
              <th class="py-2 pr-4">Admin</th>
              <th class="py-2 pr-4">Total</th>
              <th class="py-2 pr-4">Watching</th>
              <th class="py-2 pr-4">To watch</th>
              <th class="py-2 pr-4">Watched</th>
              <th class="py-2 pr-4">Upcoming</th>
              <th class="py-2 pr-4">Avg score</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id" class="border-b last:border-0">
              <td class="py-2 pr-4 font-medium">{{ u.username || '—' }}</td>
              <td class="py-2 pr-4">{{ u.email }}</td>
              <td class="py-2 pr-4">
                <span :class="u.is_admin ? 'text-emerald-700' : 'text-gray-500'">
                  {{ u.is_admin ? 'Yes' : 'No' }}
                </span>
              </td>
              <td class="py-2 pr-4">{{ u.stats?.total ?? 0 }}</td>
              <td class="py-2 pr-4">{{ u.stats?.watching ?? 0 }}</td>
              <td class="py-2 pr-4">{{ u.stats?.to_watch ?? 0 }}</td>
              <td class="py-2 pr-4">{{ u.stats?.watched ?? 0 }}</td>
              <td class="py-2 pr-4">{{ u.stats?.upcoming ?? 0 }}</td>
              <td class="py-2 pr-4">{{ u.stats?.avg_score ?? '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ middleware: ['admin-only'], layout: 'wide' })

const { apiFetch } = useApi()
const users = ref([])
const loading = ref(false)
const error = ref('')

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
</script>
