<template>
  <a
    :href="link"
    target="_blank"
    rel="noopener noreferrer"
    class="inline-flex items-center gap-2 px-4 py-2 font-semibold transition-all duration-300 transform rounded-full group"
    :class="[
      variant === 'outline' 
        ? 'bg-transparent border border-pink-500 text-pink-500 hover:bg-pink-500 hover:text-white' 
        : 'bg-gradient-to-r from-pink-500 to-rose-500 text-white shadow-lg shadow-pink-500/30 hover:shadow-pink-500/50 hover:-translate-y-0.5'
    ]"
  >
    <span class="text-lg group-hover:animate-bounce">☕</span>
    <span>{{ label }}</span>
  </a>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'solid', // 'solid' | 'outline'
  },
  label: {
    type: String,
    default: 'Sostienici',
  },
  link: {
    type: String,
    default: 'https://ko-fi.com/S6S21Q9HR0', 
  }
})
</script>
