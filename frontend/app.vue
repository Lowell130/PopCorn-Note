<template>
  <NuxtLayout>
    <!-- forza il remount della pagina ad ogni cambio di route -->
    <NuxtPage :key="$route.fullPath" />
    <!-- Bot AI Assistente fluttuante globale -->
    <PopcornBot />
  </NuxtLayout>
</template>

<script setup>
const { init } = useAuth()
onMounted(() => {
  init()
})
</script>
