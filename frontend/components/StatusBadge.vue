<template>
  <span :class="classes" class="absolute inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium top-3 end-1">
    <slot>{{ label }}</slot>
  </span>
</template>

<script setup>
const props = defineProps({ status: { type: String, required: true } })

const map = {
  to_watch: { label: 'DA VEDERE', cls: 'bg-red-100 text-red-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-sm dark:bg-red-900 dark:text-red-300' },
  watched:  { label: 'VISTO',     cls: 'bg-green-100 text-green-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm dark:bg-green-900 dark:text-green-300' },
  upcoming: { label: 'IN USCITA', cls: 'bg-purple-100 text-purple-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-sm dark:bg-purple-900 dark:text-purple-300' },
  watching: { label: 'IN VISIONE', cls: 'bg-pink-100 text-pink-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-sm dark:bg-pink-900 dark:text-pink-300' },
}
const label = computed(() => map[props.status]?.label || props.status)
const classes = computed(() => map[props.status]?.cls || 'bg-gray-100 text-gray-800')
</script>
