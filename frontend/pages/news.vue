<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h1 class="text-2xl font-semibold mb-4">Film & Serie più popolari</h1>
      <!-- <NuxtLink to="/" class="text-sm text-blue-600 hover:underline">← Torna alla dashboard</NuxtLink> -->
    </div>

    <TrendingNews @prefill="onPrefill" />

    <!-- Form aggiunta (riusa AddMovieForm) -->
    <div class="mt-6">
      <AddMovieForm v-if="showForm" :initial-data="prefillData" @added="onAdded" />
    </div>
  </div>
</template>

<script setup>
import TrendingNews from '@/components/TrendingNews.vue'
import AddMovieForm from '@/components/AddMovieForm.vue'

const prefillData = ref(null)
const showForm = ref(false)

function onPrefill(data){
  prefillData.value = data
  showForm.value = true
}

function onAdded(){
  showForm.value = false
}
definePageMeta({
  layout: 'wide'
})
</script>
