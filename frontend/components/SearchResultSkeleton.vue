<template>
  <li class="py-3 px-3 flex items-start gap-3 rounded-lg border border-gray-100 bg-white">
    <!-- Poster skeleton -->
    <SkeletonLoader width="4rem" height="6rem" borderRadius="0.25rem" class="flex-shrink-0" />

    <div class="min-w-0 flex-1 flex flex-col gap-2">
      <!-- Title + Tags -->
      <div class="space-y-1">
        <div class="flex items-center gap-2">
           <SkeletonLoader width="30px" height="16px" borderRadius="999px" />
           <SkeletonLoader width="40%" height="20px" />
           <SkeletonLoader width="40px" height="14px" class="ml-auto" />
        </div>
        
        <!-- Director -->
        <SkeletonLoader width="25%" height="14px" />

        <!-- Overview -->
        <SkeletonLoader width="90%" height="12px" />
        <SkeletonLoader width="80%" height="12px" />
      </div>

      <!-- Actions -->
      <div class="flex items-center justify-end gap-2 mt-1">
         <SkeletonLoader width="80px" height="28px" borderRadius="999px" />
         <SkeletonLoader width="60px" height="28px" borderRadius="999px" />
      </div>
    </div>
  </li>
</template>

<script setup>
import SkeletonLoader from './SkeletonLoader.vue'
</script>
