<!-- pages/login.vue -->
<template>
  <div class="max-w-md mx-auto bg-white text-black rounded-2xl p-6 shadow">
    <h1 class="text-2xl font-semibold mb-6">Accedi</h1>
    <form @submit.prevent="submit" class="space-y-4">
      <input
        v-model="email"
        type="email"
        placeholder="Email"
       class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        required
      />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
       class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        required
      />
      <button
        class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"
      >
        Login
      </button>
    </form>
  </div>
</template>

<script setup>
const email = ref("")       // vuoto di default
const password = ref("")    // vuoto di default
const { login } = useAuth()

async function submit() {
  try {
    await login({ email: email.value, password: password.value })
    navigateTo("/")
  } catch (e) {
    alert("Login fallito")
    console.error(e)
  }
}
</script>
