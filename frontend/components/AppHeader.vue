<template>
  <nav class="border-b border-white/10 bg-white/80 dark:bg-gray-900/80 backdrop-blur sticky top-0 z-10">
    <div class="max-w-5xl mx-auto px-4 py-3 flex flex-wrap items-center justify-between">
      <!-- Brand -->
      <NuxtLink to="/" class="flex items-center space-x-3 rtl:space-x-reverse">
        <span class="text-2xl">🍿</span>
        <span class="self-center text-xl font-semibold whitespace-nowrap text-black dark:text-white">
          PopCornNote
        </span>
      </NuxtLink>

      <!-- Hamburger -->
      <button
        type="button"
        class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-600 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-300 dark:hover:bg-gray-800 dark:focus:ring-gray-700"
        :aria-expanded="open ? 'true' : 'false'"
        aria-controls="navbar-default"
        @click="open = !open"
      >
        <span class="sr-only">Apri menù</span>
        <svg class="w-5 h-5" aria-hidden="true" fill="none" viewBox="0 0 17 14">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M1 1h15M1 7h15M1 13h15" />
        </svg>
      </button>

      <!-- Menu -->
      <div
        :class="[
          'w-full md:block md:w-auto',
          open ? 'block' : 'hidden'
        ]"
        id="navbar-default"
      >
        <ul
          class="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-white/80 md:flex-row md:space-x-6 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-transparent
                 dark:bg-gray-800/80 md:dark:bg-transparent dark:border-gray-700"
        >
          <!-- Non loggato -->
          <template v-if="!isLoggedIn">
            <li>
              <NuxtLink
                to="/login"
                class="block py-2 px-3 text-gray-900 rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-gray-100 md:dark:hover:text-blue-400 dark:hover:bg-gray-800 md:dark:hover:bg-transparent"
                @click="closeOnMobile"
              >
                Login
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                to="/register"
                class="block py-2 px-3 text-gray-900 rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-gray-100 md:dark:hover:text-blue-400 dark:hover:bg-gray-800 md:dark:hover:bg-transparent"
                @click="closeOnMobile"
              >
                Register
              </NuxtLink>
            </li>
          </template>

          <!-- Loggato -->
          <template v-else>
            <li>
              <NuxtLink
                to="/"
                class="block py-2 px-3 text-blue-700 md:text-blue-700 md:p-0 dark:text-white md:dark:text-blue-400"
                @click="closeOnMobile"
              >
                Dashboard
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                to="/test"
                class="block py-2 px-3 text-gray-900 rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-gray-100 md:dark:hover:text-blue-400 dark:hover:bg-gray-800 md:dark:hover:bg-transparent"
                @click="closeOnMobile"
              >
                Dashboard 2
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                to="/news"
                class="block py-2 px-3 text-gray-900 rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-gray-100 md:dark:hover:text-blue-400 dark:hover:bg-gray-800 md:dark:hover:bg-transparent"
                @click="closeOnMobile"
              >
                News
              </NuxtLink>
            </li>
            <li class="md:pl-2">
              <button
                class="w-full md:w-auto text-white bg-indigo-600 hover:bg-indigo-700 focus:ring-4 focus:outline-none focus:ring-indigo-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-indigo-600 dark:hover:bg-indigo-700 dark:focus:ring-indigo-800"
                @click="onLogout"
              >
                Logout
              </button>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
const open = ref(false)

const token = useCookie('token', { sameSite: 'lax', path: '/', watch: true })
const isLoggedIn = computed(() => !!token.value)

const { logout } = useAuth()
function onLogout() {
  if (isLoggedIn.value) logout()
  open.value = false
}

function closeOnMobile() {
  // chiude il menu dopo un click su voce in mobile
  if (window.innerWidth < 768) open.value = false
}
</script>
