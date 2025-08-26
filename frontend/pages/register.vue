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
          class="w-full border rounded p-2"
          required
        />
      </div>
      <div class="mb-3">
        <label class="block mb-1">Username</label>
        <input
          v-model="username"
          type="text"
          class="w-full border rounded p-2"
          required
        />
      </div>
      <div class="mb-5">
        <label class="block mb-1">Password</label>
        <input
          v-model="password"
          type="password"
          class="w-full border rounded p-2"
          required
        />
      </div>
      <button class="w-full bg-cinema text-white rounded p-2">
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