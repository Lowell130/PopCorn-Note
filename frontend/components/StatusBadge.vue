<template>
  <span :class="classes" class="absolute inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium top-2 end-1">
    <slot>{{ label }}</slot>
  </span>
</template>

<script setup>
const props = defineProps({ status: { type: String, required: true } })

const map = {
  to_watch: { label: 'DA VEDERE', cls: 'bg-green-100 text-green-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm dark:bg-green-900 dark:text-green-300' },
  watched:  { label: 'Visto',     cls: 'bg-green-100 text-green-800' },
  upcoming: { label: 'In uscita', cls: 'bg-amber-100 text-amber-800' },
}
const label = computed(() => map[props.status]?.label || props.status)
const classes = computed(() => map[props.status]?.cls || 'bg-gray-100 text-gray-800')
</script>
