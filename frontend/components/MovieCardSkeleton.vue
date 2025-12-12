<template>
  <article class="w-full">
    <div class="rounded-lg bg-white p-4 shadow-sm dark:border-gray-700 dark:bg-gray-800 w-full h-full flex flex-col">
      <!-- Poster area -->
      <div class="w-full aspect-[2/3] overflow-hidden rounded relative mb-4">
        <SkeletonLoader height="100%" width="100%" borderRadius="0" />
      </div>

      <!-- Content area -->
      <div class="flex-1 space-y-3">
         <!-- Tags line (Genre / Status) -->
         <div class="flex items-center justify-between gap-2">
            <SkeletonLoader width="40px" height="20px" borderRadius="4px" />
            <SkeletonLoader width="60px" height="20px" borderRadius="12px" />
         </div>

         <!-- Title -->
         <SkeletonLoader width="80%" height="24px" />
         
         <!-- Meta (Year, Duration/Rating) -->
         <div class="flex items-center justify-between mt-2">
            <SkeletonLoader width="30%" height="16px" />
            <SkeletonLoader width="20%" height="16px" />
         </div>

         <!-- Director / Extra info -->
         <div class="mt-2">
            <SkeletonLoader width="50%" height="14px" />
         </div>

         <!-- Buttons area -->
         <div class="mt-4 flex items-center justify-between gap-4">
            <SkeletonLoader width="45%" height="36px" borderRadius="8px" />
            <SkeletonLoader width="45%" height="36px" borderRadius="8px" />
         </div>
      </div>
    </div>
  </article>
</template>

<script setup>
import SkeletonLoader from './SkeletonLoader.vue'
</script>
