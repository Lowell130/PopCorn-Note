<!-- app.vue -->
<template>
  <NuxtLayout>
    <!-- forza il remount della pagina ad ogni cambio di route -->
    <NuxtPage :key="$route.fullPath" />
  </NuxtLayout>
</template>

<script setup>
const { init } = useAuth()
onMounted(() => {
  init()
})
</script>
