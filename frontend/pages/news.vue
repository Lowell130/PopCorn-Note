<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-extrabold text-white tracking-tight mb-2">Film & Serie più popolari</h1>
    </div>

    <!-- Guide Banner (Explain News/Trending) -->
    <div class="bg-purple-950/20 border border-purple-500/30 p-6 rounded-2xl flex items-start gap-4 shadow-xl backdrop-blur-md mb-8">
      <div class="p-3 bg-purple-500/10 border border-purple-500/20 rounded-xl text-purple-300 flex-shrink-0 select-none">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      </div>
      <div class="space-y-1 text-left">
        <h4 class="text-sm font-bold text-white">Scopri le tendenze globali</h4>
        <p class="text-xs text-gray-300 leading-relaxed">
          Questa sezione mostra in tempo reale i film e le serie TV più popolari e cliccati in tutto il mondo nelle ultime 24 ore o nell'ultima settimana, direttamente dalle API ufficiali di TMDb. 
          Esplora le novità per trovare ispirazione per le tue prossime visioni. Se trovi qualcosa che ti interessa, clicca su <span class="text-green-400 font-semibold">+ Aggiungi</span> per importarlo all'istante nella tua Dashboard e personalizzarlo!
        </p>
      </div>
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
