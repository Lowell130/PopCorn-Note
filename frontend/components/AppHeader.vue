<template>
  <nav 
    class="fixed top-0 w-full z-50 transition-all duration-300 border-b border-white/5 bg-black/70 backdrop-blur-xl"
  >
    <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
      
      <!-- Brand -->
      <NuxtLink to="/" class="group flex items-center gap-3 relative z-[70]">
        <span class="text-3xl transform group-hover:scale-110 transition-transform duration-300">🍿</span>
        <span class="font-bold text-xl tracking-tight text-white group-hover:text-blue-400 transition-colors">
          PopCornNote
        </span>
      </NuxtLink>

      <!-- Desktop Menu -->
      <div class="hidden md:flex items-center gap-8">
        <!-- Links -->
        <template v-if="isLoggedIn">
          <NuxtLink to="/" class="text-sm font-medium text-gray-400 hover:text-white transition-colors duration-200 uppercase tracking-wider" active-class="!text-white">Dashboard</NuxtLink>
          <NuxtLink to="/news" class="text-sm font-medium text-gray-400 hover:text-white transition-colors duration-200 uppercase tracking-wider" active-class="!text-white">News</NuxtLink>
          <NuxtLink to="/stats" class="text-sm font-medium text-gray-400 hover:text-white transition-colors duration-200 uppercase tracking-wider" active-class="!text-white">Statistiche</NuxtLink>
          <NuxtLink to="/community" class="text-sm font-medium text-gray-400 hover:text-white transition-colors duration-200 uppercase tracking-wider" active-class="!text-white">Community</NuxtLink>
          <NuxtLink v-if="isAdmin" to="/admin/users" class="text-sm font-medium text-gray-400 hover:text-white transition-colors duration-200 uppercase tracking-wider text-yellow-400 hover:!text-yellow-300" active-class="!text-white">Admin</NuxtLink>
        </template>

        <!-- Auth Buttons -->
        <div class="flex items-center gap-4 ml-4 pl-4 border-l border-white/10">
          <template v-if="!isLoggedIn">
            <NuxtLink to="/login" class="text-sm font-medium text-gray-400 hover:text-white transition-colors duration-200 uppercase tracking-wider" active-class="!text-white">Accedi</NuxtLink>
            <NuxtLink to="/register" class="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-full text-sm font-medium transition-all shadow-lg shadow-blue-900/20 hover:shadow-blue-900/40">
              Inizia gratis
            </NuxtLink>
          </template>
          <template v-else>
            <NuxtLink to="/settings" class="text-sm font-medium text-gray-400 hover:text-white transition-colors duration-200 uppercase tracking-wider" active-class="!text-white">Impostazioni</NuxtLink>
            <button @click="onLogout" class="px-4 py-1.5 border border-white/20 hover:bg-white/10 text-white rounded-full text-xs font-medium transition-all">
              Logout
            </button>
          </template>
        </div>
      </div>

      <!-- Mobile Hamburger -->
      <button 
        class="md:hidden relative z-[70] w-10 h-10 flex flex-col justify-center items-center gap-1.5 focus:outline-none"
        @click="open = !open"
      >
        <span :class="['w-6 h-0.5 bg-white rounded-full transition-all duration-300', open ? 'rotate-45 translate-y-2' : '']"></span>
        <span :class="['w-6 h-0.5 bg-white rounded-full transition-all duration-300', open ? 'opacity-0' : '']"></span>
        <span :class="['w-6 h-0.5 bg-white rounded-full transition-all duration-300', open ? '-rotate-45 -translate-y-2' : '']"></span>
      </button>
    </div>

    <!-- Mobile Menu Teleported to Body -->
    <Teleport to="body">
      <!-- Mobile Backdrop -->
      <Transition
        enter-active-class="transition-opacity duration-300 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-200 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div 
          v-if="open" 
          class="fixed inset-0 z-[5000] bg-black/60 backdrop-blur-sm md:hidden"
          @click="open = false"
        ></div>
      </Transition>

      <!-- Mobile Side Drawer -->
      <Transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="-translate-x-full"
        enter-to-class="translate-x-0"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="translate-x-0"
        leave-to-class="-translate-x-full"
      >
        <div 
          v-if="open" 
          class="fixed inset-y-0 left-0 z-[5001] w-4/5 max-w-sm bg-gray-900 border-r border-white/10 shadow-3xl md:hidden overflow-y-auto"
        >
          <div class="flex flex-col p-6 pt-10 space-y-2">
            <!-- Close Button Header in Drawer for easier closing -->
             <div class="flex justify-between items-center mb-6 pb-4 border-b border-white/5">
                <span class="text-xl font-bold text-white tracking-tight">PopCornNote</span>
                <button @click="open = false" class="p-2 text-gray-400 hover:text-white transition">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
            </div>

            <template v-if="!isLoggedIn">
              <div class="space-y-4 px-2">
                 <NuxtLink to="/login" class="text-xl font-bold text-white block" @click="closeOnMobile">Accedi</NuxtLink>
                 <NuxtLink to="/register" class="text-center w-full block px-6 py-3 bg-blue-600 rounded-full text-white font-bold shadow-lg" @click="closeOnMobile">Inizia gratis</NuxtLink>
              </div>
            </template>

            <template v-else>
              <div class="px-3 mb-4">
                <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Menu</span>
              </div>
              
              <NuxtLink to="/" class="group flex items-center px-3 py-3 text-lg font-medium text-gray-300 rounded-xl hover:bg-white/10 hover:text-white transition-all" @click="closeOnMobile">
                Dashboard
              </NuxtLink>
              <NuxtLink to="/news" class="group flex items-center px-3 py-3 text-lg font-medium text-gray-300 rounded-xl hover:bg-white/10 hover:text-white transition-all" @click="closeOnMobile">
                News
              </NuxtLink>
              <NuxtLink to="/stats" class="group flex items-center px-3 py-3 text-lg font-medium text-gray-300 rounded-xl hover:bg-white/10 hover:text-white transition-all" @click="closeOnMobile">
                 Statistiche
              </NuxtLink>
              <NuxtLink to="/community" class="group flex items-center px-3 py-3 text-lg font-medium text-gray-300 rounded-xl hover:bg-white/10 hover:text-white transition-all" @click="closeOnMobile">
                 Community
              </NuxtLink>
               <NuxtLink v-if="isAdmin" to="/admin/users" class="group flex items-center px-3 py-3 text-lg font-medium text-yellow-500 rounded-xl hover:bg-yellow-500/10 transition-all" @click="closeOnMobile">
                 Admin Panel
              </NuxtLink>

              <div class="h-px bg-white/10 my-4 mx-3"></div>

              <div class="px-3 mb-2">
                <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Account</span>
              </div>

              <NuxtLink to="/settings" class="group flex items-center px-3 py-3 text-base font-medium text-gray-400 rounded-xl hover:bg-white/5 hover:text-white transition-all" @click="closeOnMobile">
                Impostazioni
              </NuxtLink>
              
              <button @click="onLogout" class="w-full text-left group flex items-center px-3 py-3 text-base font-medium text-red-500 rounded-xl hover:bg-red-500/10 transition-all">
                Esci
              </button>
            </template>
          </div>
        </div>
      </Transition>
    </Teleport>
  </nav>
</template>

<script setup>
const open = ref(false)
const { isAdmin, logout } = useAuth()
// Utilizzo cookie per reattività immediata dello stato loggedIn
const token = useCookie('token', { sameSite: 'lax', path: '/', watch: true })
const isLoggedIn = computed(() => !!token.value)

function onLogout() {
  if (isLoggedIn.value) logout()
  open.value = false
}

function closeOnMobile() {
  open.value = false
}

// Disable scroll when mobile menu is open
watch(open, (val) => {
  if (import.meta.client) {
    document.body.style.overflow = val ? 'hidden' : ''
  }
})
</script>

<style scoped>
/* Removed @apply rules to prevent build errors. Styles are now inline. */
</style>
