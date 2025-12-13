<template>
  <div class="min-h-screen bg-night ">
    <AppHeader />
    <!-- main più largo -->
    <main class="max-w-7xl mx-auto px-4 py-6 pt-24">
      <slot />
    </main>
    <AppFooter />

    <!-- Toast globale -->
    <ClientOnly>
      <Teleport to="body">
        <Transition name="fade">
          <div
            v-if="showToast"
            class="fixed bottom-4 left-4 px-4 py-2 rounded shadow-lg z-[9999]"
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
const showToast = computed(() => {
  const m = toast.msg.value
  return typeof m === 'string' && m.trim().length > 0
})
</script>
