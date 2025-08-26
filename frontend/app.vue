<!-- app.vue -->
<template>
  <NuxtLayout>
    <!-- forza il remount della pagina ad ogni cambio di route -->
    <NuxtPage :key="$route.fullPath" />
  </NuxtLayout>
</template>