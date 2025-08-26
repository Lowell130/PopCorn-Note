<!-- pages/login.vue -->
<template>
  <div class="max-w-md mx-auto bg-white text-black rounded-2xl p-6 shadow">
    <h1 class="text-2xl font-semibold mb-4">Accedi</h1>
    <form @submit.prevent="submit">
      <div class="mb-4">
        <label class="block mb-1">Email</label>
        <input
          v-model="email"
          type="email"
          class="w-full border rounded p-2"
          required
        />
      </div>
      <div class="mb-6">
        <label class="block mb-1">Password</label>
        <input
          v-model="password"
          type="password"
          class="w-full border rounded p-2"
          required
        />
      </div>
      <button class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">Login</button>
    </form>
  </div>
</template>


<script setup>
const email = ref("test@example.com");
const password = ref("123456");
const { login } = useAuth();

async function submit() {
  try {
    await login({ email: email.value, password: password.value });
    navigateTo("/");
  } catch (e) {
    alert("Login fallito");
    console.error(e);
  }
}
</script>