<template>
  <div class="min-h-screen bg-night text-white relative overflow-hidden">
    <!-- Background Gradient Lights (Cinematic Animated Spotlights) -->
    <div class="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -left-40 w-96 h-96 rounded-full bg-purple-600/10 blur-3xl animate-glow-slow-1"></div>
      <div class="absolute top-1/2 -right-40 w-96 h-96 rounded-full bg-blue-600/10 blur-3xl animate-glow-slow-2"></div>
      <div class="absolute -bottom-40 left-1/3 w-96 h-96 rounded-full bg-emerald-600/10 blur-3xl animate-glow-slow-3"></div>
    </div>

    <AppHeader />
    <main class="pt-20 relative z-10 w-full">
      <slot />
    </main>
    <AppFooter />

    <!-- Toast globale -->
    <ClientOnly>
      <Teleport to="body">
        <Transition name="fade">
          <div
            v-if="showToast"
            class="fixed bottom-4 right-4 px-4 py-2 rounded shadow-lg z-[9999]"
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

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity .2s }
.fade-enter-from, .fade-leave-to { opacity: 0 }

/* Animated Spotlights keyframes */
@keyframes glow-1 {
  0%, 100% { transform: translate(0px, 0px) scale(1); opacity: 0.7; }
  33% { transform: translate(40px, -50px) scale(1.15); opacity: 0.9; }
  66% { transform: translate(-30px, 30px) scale(0.9); opacity: 0.6; }
}
@keyframes glow-2 {
  0%, 100% { transform: translate(0px, 0px) scale(1); opacity: 0.6; }
  50% { transform: translate(-50px, 60px) scale(1.2); opacity: 0.95; }
}
@keyframes glow-3 {
  0%, 100% { transform: translate(0px, 0px) scale(1); opacity: 0.7; }
  40% { transform: translate(60px, -40px) scale(1.1); opacity: 0.85; }
}

.animate-glow-slow-1 {
  animation: glow-1 16s infinite ease-in-out;
}
.animate-glow-slow-2 {
  animation: glow-2 20s infinite ease-in-out;
}
.animate-glow-slow-3 {
  animation: glow-3 24s infinite ease-in-out;
}
</style>
