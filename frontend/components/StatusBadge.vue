<template>
  <!-- <span :class="classes" class="absolute inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium top-3 end-1"> -->
     <span :class="classes" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium">
    <slot>{{ label }}</slot>
  </span>
</template>

<script setup>
const props = defineProps({ status: { type: String, required: true } })

const map = {
  to_watch: { label: 'DA VEDERE', cls: 'bg-sky-500/10 border border-sky-500/20 text-sky-400 text-[10px] font-bold px-2 py-0.5 rounded-md shadow-sm select-none' },
  watched:  { label: 'VISTO',     cls: 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-bold px-2 py-0.5 rounded-md shadow-sm select-none' },
  upcoming: { label: 'IN USCITA', cls: 'bg-purple-500/10 border border-purple-500/20 text-purple-400 text-[10px] font-bold px-2 py-0.5 rounded-md shadow-sm select-none' },
  watching: { label: 'IN VISIONE', cls: 'bg-amber-500/10 border border-amber-500/20 text-amber-400 text-[10px] font-bold px-2 py-0.5 rounded-md shadow-sm select-none' }
}
const label = computed(() => map[props.status]?.label || props.status)
const classes = computed(() => map[props.status]?.cls || 'bg-gray-100 text-gray-800')
</script>
