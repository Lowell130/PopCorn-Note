<!-- pages/register.vue -->
<template>
  <div class="max-w-md mx-auto bg-white text-black rounded-2xl p-6 shadow">
    <h1 class="text-2xl font-semibold mb-4">Registrati</h1>
    <form @submit.prevent="submit">
      <div class="mb-3">
        <label class="block mb-1">Email</label>
        <input
          v-model="email"
          type="email"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          required
        />
      </div>
      <div class="mb-3">
        <label class="block mb-1">Username</label>
        <input
          v-model="username"
          type="text"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          required
        />
      </div>
      <div class="mb-5">
        <label class="block mb-1">Password</label>
        <input
          v-model="password"
          type="password"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          required
        />
      </div>
      <button class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
        Crea account
      </button>
    </form>
  </div>
</template>


<script setup>
const email = ref("");
const username = ref("");
const password = ref("");
const { register } = useAuth();

async function submit() {
  try {
    await register({
      email: email.value,
      username: username.value,
      password: password.value,
    });
    navigateTo("/login");
  } catch (e) {
    alert("Registrazione fallita");
    console.error(e);
  }
}
</script>