<template>
  <div class="min-h-screen bg-night text-white">
    <AppHeader />
    <main class="max-w-5xl mx-auto px-4 py-6">
      <slot />
    </main>
<AppFooter />
    <!-- Toast globale -->
    <ClientOnly>
      <Teleport to="body">
        <Transition name="fade">
          <div
            v-if="showToast"
            class="fixed bottom-4 right-4 px-4 py-2 rounded shadow-lg"
            :class="toast.type === 'success'
              ? 'bg-green-600 text-white'
              : 'bg-red-600 text-white'"
          >
            {{ toast.msg }}
          </div>
        </Transition>
      </Teleport>
    </ClientOnly>
  </div>
</template>

<script setup>
const toast = useToast()
// predicato robusto calcolato in JS (evita stringhe vuote/spazi)
const showToast = computed(() => {
  const m = toast.msg.value
  return typeof m === 'string' && m.trim().length > 0
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity .2s }
.fade-enter-from, .fade-leave-to { opacity: 0 }
</style>
