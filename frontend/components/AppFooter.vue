<template>
  <footer class="p-4 bg-white md:p-8 lg:p-10 dark:bg-gray-800">
    <div class="mx-auto max-w-screen-xl text-center">
      <!-- Logo + nome -->
      <!-- <a href="/" class="flex justify-center items-center text-2xl font-semibold text-gray-900 dark:text-white">
        <svg class="mr-2 h-8 w-8 text-yellow-500" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2C9.243 2 7 4.243 7 7c0 1.654 1.346 3 3 3h1v11a1 1 0 1 0 2 0V10h1c1.654 0 3-1.346 3-3 0-2.757-2.243-5-5-5z"/>
        </svg>
        PopCornNote
      </a> -->

        <NuxtLink to="/" class="flex justify-center items-center text-2xl font-semibold text-gray-900 dark:text-white">🍿 PopCornNote</NuxtLink>

      <!-- Descrizione -->
      <p class="my-6 text-gray-500 dark:text-gray-400">
        PopCornNote è la tua app per gestire film e serie TV: cerca, organizza e tieni traccia di ciò che guardi.
      </p>

      <!-- Credits -->
      <span class="text-sm text-gray-500 sm:text-center dark:text-gray-400">
        © {{ new Date().getFullYear() }} PopCornNote. Tutti i diritti riservati.
      </span>
    </div>

    <!-- Pulsante Torna su -->
    <transition name="fade">
      <button
        v-if="showScrollTop"
        @click="scrollToTop"
        class="fixed bottom-6 right-6 z-50 p-3 rounded-full bg-gray-600 text-white shadow-lg hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-800"
        aria-label="Torna su"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
        </svg>
      </button>
    </transition>
  </footer>
</template>

<script setup>
const showScrollTop = ref(false)

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function handleScroll() {
  showScrollTop.value = window.scrollY > 200
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
