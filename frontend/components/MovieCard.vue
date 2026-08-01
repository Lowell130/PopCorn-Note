<!-- components/MovieCard.vue -->
<template>
  <article :class="cardClasses">
    <div
      class="text-white rounded-2xl bg-white/5 border border-white/10 p-4 shadow-lg backdrop-blur-sm w-full relative overflow-hidden"
    >
      <div class="w-full aspect-[2/3] overflow-hidden rounded-xl relative group">
        <NuxtLink target="_blank"
          v-if="movie.id"
          :to="movie.kind === 'tv' ? `/tv/${movie.id}` : `/movies/${movie.id}`"
          class="block h-full w-full"
        >
          <img
            v-if="movie.poster_url"
            :src="movie.poster_url"
            alt=""
            class="w-full h-full object-cover transition duration-500 ease-in-out group-hover:scale-105 group-hover:brightness-30"
            loading="lazy"
            decoding="async"
          />
          <!-- Overlay descrizione -->
          <div
            v-if="movie.overview"
            class="absolute inset-0 flex items-center justify-center px-3 text-left text-xs text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300 leading-relaxed bg-black/60 backdrop-blur-xs"
          >
            {{
              movie.overview.length > 250
                ? movie.overview.slice(0, 250) + "…"
                : movie.overview
            }}
          </div>
          
          <div
            v-else
            class="absolute inset-0 flex items-center justify-center px-3 text-left text-sm text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/60"
          >
            N/A
          </div>
        </NuxtLink>

        <div
          v-else
          class="w-full h-full flex items-center justify-center text-xs text-gray-500 bg-white/5 border border-white/10"
        >
          Nessun poster
        </div>
      </div>

      <div class="pt-4">
        <div class="mb-4 flex items-center justify-between gap-4">
          <span v-if="movie.kind" :class="kindChipClass">
            {{ kindLabel }}
          </span>
          <StatusBadge :status="movie.status" />
        </div>

        <h3 class="text-md font-bold leading-snug break-words text-white hover:text-purple-400 transition-colors">
          <NuxtLink target="_blank"
            v-if="movie.id"
            :to="
              movie.kind === 'tv' ? `/tv/${movie.id}` : `/movies/${movie.id}`
            "
            class="hover:underline focus:outline-none focus:ring-2 focus:ring-purple-500/50 rounded-sm"
          >
            {{ shortTitle }}
          </NuxtLink>
          <template v-else>{{ shortTitle }}</template>
        </h3>
        
        <div class="mt-1 flex items-center justify-between text-xs text-gray-400">
          <p>
            <span v-if="movie.release_year">{{ movie.release_year }}</span>
            <span v-if="movie.kind === 'movie' && movie.runtime">
              · {{ movie.runtime }} min
            </span>
          </p>

          <!-- Voto TMDB -->
          <p v-if="tmdbScore" class="flex items-center gap-1">
            <span class="text-yellow-500">★</span>
            <span class="font-semibold">{{ tmdbScore }}</span>
          </p>
        </div>
        
        <ul class="mt-3 flex items-center gap-4 text-xs text-gray-400 border-t border-white/5 pt-3">
          <li v-if="movie.director" class="flex items-center gap-1.5 truncate">
            <span class="text-gray-500">Regia:</span>
            <NuxtLink
              :to="{ path: '/dashboard', query: { director: movie.director } }"
              class="font-semibold text-purple-400 hover:underline hover:text-purple-300 transition-colors"
            >
              {{ movie.director }}
            </NuxtLink>
          </li>
          <li v-else class="text-gray-500">
            N/A
          </li>
        </ul>

        <!-- Azioni Card (Edit/Delete) -->
        <div class="mt-4 flex items-center justify-between border-t border-white/5 pt-3">
          <!-- Nota and Tags Indicator (Bottom Left) -->
          <div class="flex items-center gap-1.5 overflow-hidden max-w-[70%]">
            <span 
              v-if="movie.note" 
              class="text-xs text-gray-500 cursor-help select-none shrink-0"
              :title="movie.note"
            >
              📝
            </span>
            <div v-if="movie.tags && movie.tags.length" class="flex gap-1 overflow-hidden">
              <NuxtLink
                v-for="t in movie.tags.slice(0, 2)"
                :key="t"
                :to="{ path: '/dashboard', query: { tag: t } }"
                class="text-[9px] font-semibold tracking-wider uppercase px-1.5 py-0.5 rounded bg-purple-500/10 border border-purple-500/20 text-purple-400 hover:bg-purple-500/20 transition-all cursor-pointer truncate max-w-[80px]"
              >
                #{{ t }}
              </NuxtLink>
            </div>
          </div>

          <div class="flex gap-2">
            <button
              @click.stop="toggleEdit"
              class="p-1 text-gray-400 hover:text-white transition"
              title="Modifica"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
            </button>
            <button
              @click.stop="remove"
              class="p-1 text-gray-400 hover:text-red-400 transition"
              title="Elimina"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Modulo Modifica Modale via Teleport -->
      <Teleport to="body">
        <Transition
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="opacity-0"
          enter-to-class="opacity-100"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div
            v-if="editing"
            class="fixed inset-0 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4 z-[9999]"
            @click.self="toggleEdit"
          >
            <div
              class="bg-slate-900 border border-white/10 rounded-2xl w-full max-w-md shadow-2xl p-6 relative flex flex-col max-h-[90vh] text-white"
            >
              <!-- Header -->
              <div class="flex justify-between items-center pb-4 border-b border-white/5 mb-4">
                <h3 class="text-base font-bold text-white uppercase tracking-wider truncate">
                  Modifica: {{ movie.title }}
                </h3>
                <button
                  @click="toggleEdit"
                  class="p-1 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <!-- Body -->
              <div class="space-y-4 overflow-y-auto pr-1 flex-1 py-1 no-scrollbar">
                <!-- Stato (Segmented button group) -->
                <div>
                  <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Stato</label>
                  <div class="grid grid-cols-2 gap-2">
                    <button
                      v-for="s in statuses"
                      :key="s.value"
                      type="button"
                      @click="draft.status = s.value"
                      :class="[
                        'px-3 py-2.5 text-xs font-semibold rounded-xl border transition-all text-center flex items-center justify-center gap-1.5',
                        draft.status === s.value
                          ? getStatusColorClass(s.value)
                          : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10 hover:text-white'
                      ]"
                    >
                      <span>{{ s.label }}</span>
                    </button>
                  </div>
                </div>

                <!-- Voto Personale (Interactive Progress Bar) -->
                <div class="space-y-1.5">
                  <div class="flex justify-between items-center">
                    <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest">Voto Personale</label>
                    <span v-if="draft.score" class="text-xs font-bold text-purple-400 bg-purple-500/10 border border-purple-500/20 px-2.5 py-0.5 rounded-md">
                      {{ draft.score }} / 10 {{ getScoreSentiment(draft.score) }}
                    </span>
                    <span v-else class="text-[10px] text-gray-500 italic">Nessun voto</span>
                  </div>
                  
                  <!-- Interactive Track -->
                  <div class="relative flex items-center h-8 bg-white/5 border border-white/10 rounded-xl overflow-hidden p-1 select-none">
                    <!-- Clickable Zones -->
                    <div
                      v-for="i in 10"
                      :key="i"
                      @click="draft.score = i"
                      class="flex-1 h-full cursor-pointer relative z-10"
                    >
                      <div class="absolute inset-y-0 right-0 w-px bg-white/5"></div>
                    </div>

                    <!-- Dynamic Fill -->
                    <div
                      class="absolute inset-y-0 left-0 bg-gradient-to-r from-purple-600 to-indigo-500 transition-all duration-200 pointer-events-none"
                      :style="{ width: draft.score ? `${draft.score * 10}%` : '0%' }"
                    >
                      <div class="absolute right-0 top-0 bottom-0 w-2 bg-white/30 blur-[2px]"></div>
                    </div>
                  </div>

                  <!-- Labels 1-10 -->
                  <div class="flex justify-between px-1 text-[9px] text-gray-500 font-semibold select-none">
                    <span
                      v-for="i in 10"
                      :key="i"
                      @click="draft.score = i"
                      class="cursor-pointer hover:text-purple-400 transition"
                      :class="{ 'text-purple-300 font-bold': draft.score === i }"
                    >
                      {{ i }}
                    </span>
                  </div>

                  <div class="flex justify-end" v-if="draft.score != null">
                    <button
                      type="button"
                      @click="draft.score = null"
                      class="text-[10px] text-red-400 hover:text-red-300 transition"
                    >
                      Rimuovi voto
                    </button>
                  </div>
                </div>



                <!-- Tagging (Categories) -->
                <div class="space-y-1.5">
                  <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest">Tag / Categorie</label>
                  <div class="flex flex-wrap gap-1.5 p-2 bg-white/5 border border-white/10 rounded-xl focus-within:border-purple-500/50 focus-within:ring-1 focus-within:ring-purple-500/50 transition-all">
                    <span
                      v-for="(t, idx) in draft.tags"
                      :key="idx"
                      class="inline-flex items-center gap-1 px-2 py-0.5 bg-purple-500/10 border border-purple-500/20 text-purple-300 text-[10px] font-medium rounded-lg"
                    >
                      {{ t }}
                      <button
                        type="button"
                        @click="removeTag(idx)"
                        class="text-purple-400 hover:text-purple-200 transition font-bold"
                      >
                        &times;
                      </button>
                    </span>
                    <input
                      v-model="newTagInput"
                      @keydown.enter.prevent="addTag"
                      @keydown.comma.prevent="addTag"
                      @blur="addTag"
                      placeholder="Scrivi tag e premi Invio..."
                      class="flex-1 min-w-[120px] bg-transparent border-0 text-white text-xs p-0.5 focus:ring-0 focus:outline-none placeholder-gray-600"
                    />
                  </div>
                </div>

                <!-- Nota -->
                <div>
                  <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Nota</label>
                  <textarea
                    v-model="draft.note"
                    rows="3"
                    class="w-full bg-white/5 border border-white/10 text-white text-xs rounded-xl p-2.5 focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all placeholder-gray-600 resize-none outline-none"
                    placeholder="Aggiungi una nota personale..."
                  ></textarea>
                </div>
              </div>

              <!-- Footer -->
              <div class="pt-4 flex justify-end gap-2 border-t border-white/5 mt-4">
                <button
                  @click="toggleEdit"
                  type="button"
                  class="px-4 py-2 text-xs font-semibold rounded-xl border border-white/10 text-gray-300 hover:bg-white/5 transition"
                >
                  Annulla
                </button>
                <button
                  @click="save"
                  :disabled="loading"
                  type="button"
                  class="px-4 py-2 text-xs font-semibold rounded-xl text-green-300 bg-green-500/10 border border-green-500/20 hover:bg-green-500/20 transition disabled:opacity-50"
                >
                  {{ loading ? 'Salvataggio...' : 'Salva' }}
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>
    </div>
  </article>
</template>

<script setup>
import StatusBadge from "@/components/StatusBadge.vue";

const props = defineProps({ movie: { type: Object, required: true } });
const emit = defineEmits(["updated", "deleted"]);

const { apiFetch } = useApi();
const toast = useToast();

const editing = ref(false);
const loading = ref(false);

const draft = reactive({
  status: props.movie.status,
  score: props.movie.score,
  liked: props.movie.liked,
  note: props.movie.note,
  tags: props.movie.tags ? [...props.movie.tags] : [],
});

const likedOptions = [
  { value: "loved", label: "Mi è piaciuto molto", short: "Amo", emoji: "❤️" },
  { value: "liked", label: "Mi è piaciuto", short: "Piace", emoji: "👍" },
  { value: "okay", label: "Carino", short: "Carino", emoji: "😐" },
  { value: "disliked", label: "Non mi è piaciuto", short: "No", emoji: "👎" },
  { value: "terrible", label: "Pessimo", short: "Pessimo", emoji: "💩" },
];

const kindLabel = computed(() =>
  props.movie.kind === "tv" ? "SERIE" : "FILM"
);
const kindChipClass = computed(() =>
  props.movie.kind === "tv"
    ? "bg-yellow-500/10 border border-yellow-500/20 text-yellow-400 text-[10px] font-bold px-2 py-0.5 rounded-md shadow-sm select-none"
    : "bg-blue-500/10 border border-blue-500/20 text-blue-400 text-[10px] font-bold px-2 py-0.5 rounded-md shadow-sm select-none"
);

const isWatched = computed(() => props.movie.status === "watched");
const cardClasses = computed(() => [
  // wrapper esterno (non grid)
  "w-full",
  isWatched.value
    ? "grayscale opacity-80 hover:grayscale-0 hover:opacity-100 transition"
    : "",
]);

const shortTitle = computed(() => {
  const t = props.movie.title || "";
  return t.length > 25 ? t.slice(0, 25) + "…" : t;
});

const directorUrl = computed(() => {
  const name = props.movie.director;
  const id = props.movie.director_id;
  if (id) return `https://www.themoviedb.org/person/${id}`;
  const q = encodeURIComponent(name || "");
  return `https://www.themoviedb.org/search?query=${q}`;
});

const newTagInput = ref("");

function addTag() {
  const tag = newTagInput.value.trim().toLowerCase();
  if (tag && !draft.tags.includes(tag)) {
    draft.tags.push(tag);
  }
  newTagInput.value = "";
}

function removeTag(index) {
  draft.tags.splice(index, 1);
}

function getStatusColorClass(value) {
  switch (value) {
    case 'to_watch':
      return 'bg-amber-500/10 border-amber-500 text-amber-400 shadow-md shadow-amber-500/10';
    case 'watched':
      return 'bg-emerald-500/10 border-emerald-500 text-emerald-400 shadow-md shadow-emerald-500/10';
    case 'upcoming':
      return 'bg-cyan-500/10 border-cyan-500 text-cyan-400 shadow-md shadow-cyan-500/10';
    case 'watching':
      return 'bg-fuchsia-500/10 border-fuchsia-500 text-fuchsia-400 shadow-md shadow-fuchsia-500/10';
    default:
      return 'bg-purple-500/10 border-purple-500 text-purple-400 shadow-md shadow-purple-500/10';
  }
}

function getScoreSentiment(score) {
  if (!score) return "";
  if (score >= 9) return "❤️ Amo";
  if (score >= 7) return "👍 Piace";
  if (score >= 5) return "😐 Carino";
  if (score >= 3) return "👎 No";
  return "💩 Pessimo";
}

function toggleEdit() {
  editing.value = !editing.value;
  if (editing.value) {
    draft.status = props.movie.status;
    draft.score = props.movie.score;
    draft.liked = props.movie.liked;
    draft.note = props.movie.note;
    draft.tags = props.movie.tags ? [...props.movie.tags] : [];
    newTagInput.value = "";
  }
}

const tmdbScore = computed(() => {
  const raw =
    props.movie.tmdb_vote ??
    props.movie.vote_average ??
    null

  if (raw == null) return null
  const num = typeof raw === 'number' ? raw : Number(raw)
  if (!Number.isFinite(num)) return null
  return num.toFixed(1)  // es: 7.8
})



async function remove() {
  if (!confirm(`Vuoi davvero eliminare "${props.movie.title}"?`)) return;
  loading.value = true;
  try {
    await apiFetch(`/movies/${props.movie.id}`, { method: "DELETE" });
    emit("deleted", props.movie.id);
    toast.show("success", "Film eliminato");
  } catch (e) {
    console.error(e);
    toast.show("error", "Errore durante l'eliminazione");
  } finally {
    loading.value = false;
  }
}

// Opzioni "Stato" — MANCAVANO
const statuses = [
  { value: "to_watch", label: "Da vedere" },
  { value: "watched", label: "Visto" },
  { value: "upcoming", label: "In uscita" },
  { value: "watching", label: "In visione" },
];

// Salvataggio — MANCAVA
async function save() {
  // Aggiunge tag in attesa di essere inseriti prima del salvataggio
  addTag();

  const score =
    draft.score === "" || draft.score == null
      ? null
      : Math.max(1, Math.min(10, Number(draft.score)));

  // Calcola il gradimento basato sul voto per rimuovere la ridondanza
  let liked = null;
  if (score != null) {
    if (score >= 9) liked = "loved";
    else if (score >= 7) liked = "liked";
    else if (score >= 5) liked = "okay";
    else if (score >= 3) liked = "disliked";
    else liked = "terrible";
  }

  const body = {
    status: draft.status,
    score: score,
    liked: liked,
    note: (draft.note ?? "").trim() === "" ? null : (draft.note ?? "").trim(),
    tags: draft.tags || [],
  };

  loading.value = true;
  try {
    const updated = await apiFetch(`/movies/${props.movie.id}`, {
      method: "PUT",
      body,
    });
    emit("updated", updated);
    editing.value = false;
    toast.show?.("success", "Salvato!");
  } catch (e) {
    console.error("save error", e);
    toast.show?.("error", "Errore durante il salvataggio");
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
