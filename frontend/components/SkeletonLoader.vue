<template>
  <div :class="['bg-gray-200 dark:bg-gray-700 animate-pulse', roundedClass]" :style="styleObject"></div>
</template>

<script setup>
const props = defineProps({
  width: { type: String, default: '100%' },
  height: { type: String, default: '1em' },
  borderRadius: { type: String, default: '0.5rem' }, // rounded-lg default
  circle: { type: Boolean, default: false }
})

const roundedClass = computed(() => props.circle ? 'rounded-full' : '')
const styleObject = computed(() => ({
  width: props.width,
  height: props.height,
  borderRadius: props.circle ? '9999px' : props.borderRadius
}))
</script>
