<template>
  <a
    :href="shareUrl"
    target="_blank"
    rel="noopener noreferrer"
    class="inline-flex items-center gap-2 px-4 py-2 bg-[#229ED9] hover:bg-[#229ED9]/90 text-white font-bold rounded-lg transition-all shadow-lg hover:shadow-[#229ED9]/30 hover:-translate-y-0.5 text-sm"
  >
    <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 0 0-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.4-1.08.39-.35-.01-1.03-.2-1.53-.37-.62-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .24z"/>
    </svg>
    <span>Condividi</span>
  </a>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  text: {
    type: String,
    default: 'Guarda questo su PopCornNote!'
  }
})

const shareUrl = computed(() => {
  if (import.meta.server) return '#' // Evita errori SSR
  const url = window.location.href
  const text = `${props.text} ${props.title}`
  return `https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`
})
</script>
