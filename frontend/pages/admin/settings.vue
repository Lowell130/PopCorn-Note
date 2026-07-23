<!-- pages/admin/settings.vue -->
<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- Breadcrumb & Header -->
    <div class="mb-8">
      <div class="flex items-center gap-3 text-sm text-gray-400 mb-2">
        <NuxtLink to="/admin/users" class="hover:text-purple-400 transition-colors">Admin</NuxtLink>
        <span>/</span>
        <span class="text-white font-medium">Impostazioni AI & Bot</span>
      </div>
      <h1 class="text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
        <span>🍿 Bot AI Settings</span>
      </h1>
      <p class="text-sm text-gray-400 mt-1">
        Gestisci la chiave API, il modello di Intelligenza Artificiale e il limite di chiamate per gli utenti FREE.
      </p>
    </div>

    <!-- Alert status -->
    <div v-if="successMsg" class="mb-6 p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-sm flex items-center gap-2">
      <span>✅</span> {{ successMsg }}
    </div>
    <div v-if="errorMsg" class="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm flex items-center gap-2">
      <span>⚠️</span> {{ errorMsg }}
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="py-12 flex flex-col items-center justify-center text-gray-400 gap-3">
      <div class="w-8 h-8 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin"></div>
      <p class="text-sm">Caricamento impostazioni di sistema...</p>
    </div>

    <!-- Form Impostazioni -->
    <form v-else @submit.prevent="saveSettings" class="space-y-6">
      <!-- Card Stato Bot AI -->
      <div class="bg-slate-900/60 border border-white/10 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-4">
        <div class="flex items-center justify-between">
          <div class="space-y-1">
            <h2 class="text-xl font-bold text-white flex items-center gap-2">
              <span>🤖</span> Stato PopCorn Bot
            </h2>
            <p class="text-xs text-gray-400">
              Attiva o disattiva l'assistente virtuale in tutto il sito.
            </p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="form.ai_bot_enabled" class="sr-only peer">
            <div class="w-11 h-6 bg-slate-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-gray-300 after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
          </label>
        </div>
      </div>

      <!-- Card Provider & API Key -->
      <div class="bg-slate-900/60 border border-white/10 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-6">
        <h2 class="text-xl font-bold text-white flex items-center gap-2">
          <span>🔑</span> AI Provider & API Key
        </h2>

        <!-- AI Provider -->
        <div>
          <label class="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">
            Provider Intelligenza Artificiale
          </label>
          <select
            v-model="form.ai_provider"
            class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all"
          >
            <option value="gemini">Google Gemini (Consigliato - Gratuito/Veloce)</option>
            <option value="openai">OpenAI (ChatGPT / GPT-4o-mini)</option>
          </select>
          <p class="text-xs text-gray-400 mt-1.5">
            Seleziona quale servizio di Intelligenza Artificiale utilizzare per il PopCorn Bot.
          </p>
        </div>

        <!-- AI Model Name -->
        <div>
          <label class="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">
            Modello AI
          </label>
          <input
            v-model="form.ai_model"
            type="text"
            placeholder="es. gemini-1.5-flash oppure gpt-4o-mini"
            class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all"
          />
          <p class="text-xs text-gray-400 mt-1.5">
            Per Gemini usa <code>gemini-1.5-flash</code>. Per OpenAI usa <code>gpt-4o-mini</code>.
          </p>
        </div>

        <!-- API Key Input -->
        <div>
          <label class="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">
            API Key {{ form.ai_provider === 'gemini' ? 'Google AI (Gemini)' : 'OpenAI' }}
          </label>
          <div class="relative">
            <input
              v-model="form.ai_api_key"
              :type="showKey ? 'text' : 'password'"
              placeholder="Inserisci la tua API Key..."
              class="w-full bg-slate-950 border border-white/10 rounded-xl pl-4 pr-12 py-3 text-white text-sm focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all font-mono"
            />
            <button
              type="button"
              @click="showKey = !showKey"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white p-1"
            >
              {{ showKey ? '🙈' : '👁️' }}
            </button>
          </div>
          <div class="mt-2 flex items-center justify-between text-xs">
            <span v-if="apiKeyStatus" class="text-emerald-400 font-medium">
              ✓ Chiave attualmente impostata: {{ maskedApiKey }}
            </span>
            <span v-else class="text-amber-400 font-medium">
              ⚠️ Nessuna chiave salvata (il bot userà risposte di esempio mock)
            </span>
            <a
              v-if="form.ai_provider === 'gemini'"
              href="https://aistudio.google.com/app/apikey"
              target="_blank"
              class="text-purple-400 hover:underline flex items-center gap-1"
            >
              Ottieni API Key Gemini gratis ↗
            </a>
            <a
              v-else
              href="https://platform.openai.com/api-keys"
              target="_blank"
              class="text-purple-400 hover:underline flex items-center gap-1"
            >
              Ottieni API Key OpenAI ↗
            </a>
          </div>
        </div>
      </div>

      <!-- Card Limiti di Utilizzo (Rate Limiting) -->
      <div class="bg-slate-900/60 border border-white/10 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-6">
        <h2 class="text-xl font-bold text-white flex items-center gap-2">
          <span>🛡️</span> Rate Limiting & Protezione Consumi
        </h2>

        <div>
          <label class="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">
            Limite Richieste Giornaliere per Utenti FREE / Non-Admin
          </label>
          <div class="flex items-center gap-4">
            <input
              v-model.number="form.ai_daily_limit_free"
              type="number"
              min="1"
              max="50"
              class="w-32 bg-slate-950 border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all font-bold text-center"
            />
            <span class="text-sm text-gray-300">richiesta/e al giorno per utente</span>
          </div>
          <p class="text-xs text-gray-400 mt-2">
            Per evitare costi eccessivi dell'API, gli utenti non-admin potranno effettuare solo questo numero di richieste al PopCorn Bot nelle 24 ore. Gli utenti Admin hanno sempre chiamate illimitate.
          </p>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex items-center justify-end gap-4">
        <NuxtLink
          to="/admin/users"
          class="px-5 py-2.5 border border-white/10 rounded-xl text-sm font-semibold text-gray-300 hover:bg-white/5 transition-all"
        >
          Annulla
        </NuxtLink>
        <button
          type="submit"
          :disabled="saving"
          class="px-6 py-2.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white rounded-xl text-sm font-bold shadow-lg shadow-purple-600/30 transition-all flex items-center gap-2 disabled:opacity-50"
        >
          <span v-if="saving" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
          <span>{{ saving ? 'Salvataggio...' : 'Salva Impostazioni' }}</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

definePageMeta({
  middleware: ['admin-only']
})

const { apiFetch } = useApi()

const loading = ref(true)
const saving = ref(false)
const showKey = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

const apiKeyStatus = ref(false)
const maskedApiKey = ref('')

const form = ref({
  ai_provider: 'gemini',
  ai_api_key: '',
  ai_model: 'gemini-2.0-flash',
  ai_daily_limit_free: 1,
  ai_bot_enabled: true
})

const fetchSettings = async () => {
  loading.value = true
  errorMsg.value = ''
  try {
    const data = await apiFetch('/admin/settings')
    if (data) {
      form.value.ai_provider = data.ai_provider || 'gemini'
      form.value.ai_model = data.ai_model || 'gemini-1.5-flash'
      form.value.ai_daily_limit_free = data.ai_daily_limit_free || 1
      form.value.ai_bot_enabled = data.ai_bot_enabled !== false
      apiKeyStatus.value = data.ai_api_key_set
      maskedApiKey.value = data.ai_api_key_masked
      if (data.ai_api_key_set) {
        form.value.ai_api_key = data.ai_api_key_masked
      }
    }
  } catch (err) {
    errorMsg.value = err?.data?.detail || 'Errore durante il recupero delle impostazioni Admin'
  } finally {
    loading.value = false
  }
}

const saveSettings = async () => {
  saving.value = true
  successMsg.value = ''
  errorMsg.value = ''

  try {
    const res = await apiFetch('/admin/settings', {
      method: 'POST',
      body: form.value
    })
    successMsg.value = res.message || 'Impostazioni salvate con successo!'
    await fetchSettings()
  } catch (err) {
    errorMsg.value = err?.data?.detail || 'Impossibile salvare le impostazioni'
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchSettings()
})
</script>
