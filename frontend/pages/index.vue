<!-- pages/index.vue — pagina d'ingresso: solo accesso -->
<template>
  <div class="min-h-[75vh] flex items-center justify-center px-4">
    <div class="text-center space-y-8">
      <div class="space-y-3">
        <span class="text-6xl block select-none" aria-hidden="true">🍿</span>
        <h1 class="text-4xl sm:text-5xl font-black tracking-tight text-white">PopCornNote</h1>
      </div>
      <NuxtLink
        :to="isLoggedIn ? '/dashboard' : '/login'"
        class="inline-block px-10 py-4 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/40 text-purple-200 font-bold rounded-2xl shadow-xl transition-all backdrop-blur-md hover:scale-105 duration-200"
      >
        {{ isLoggedIn ? 'Vai alla dashboard' : 'Accedi' }}
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'landing'
})

const { isLoggedIn } = useAuth()

useSeoMeta({
  title: 'PopCornNote',
  ogTitle: 'PopCornNote',
  description: 'PopCornNote — area riservata.',
  ogDescription: 'PopCornNote — area riservata.',
  ogImage: 'https://www.popcornote.com/og-image.jpg',
  ogUrl: 'https://www.popcornote.com',
  twitterCard: 'summary_large_image',
  robots: 'noindex, nofollow, noarchive',
})

</script>
