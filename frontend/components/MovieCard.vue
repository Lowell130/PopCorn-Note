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
          <!-- Nota icon indicator -->
          <span 
            v-if="movie.note" 
            class="text-xs text-gray-500 cursor-help"
            :title="movie.note"
          >
            📝 Nota
          </span>
          <span v-else></span>

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

      <!-- Modulo Modifica Inline Overlay -->
      <Transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0 translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-2"
      >
        <div
          v-if="editing"
          class="absolute inset-0 bg-slate-950/95 backdrop-blur-md p-4 flex flex-col justify-between z-35"
        >
          <div class="space-y-4 overflow-y-auto pr-1">
            <h4 class="text-sm font-bold text-white uppercase tracking-wider">Modifica Film</h4>
            
            <div class="space-y-3">
              <div>
                <label class="block text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-1">Stato</label>
                <select
                  v-model="draft.status"
                  class="w-full bg-white/5 border border-white/10 text-white text-xs rounded-xl p-2 focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all [&>option]:bg-slate-950"
                >
                  <option v-for="s in statuses" :key="s.value" :value="s.value">
                    {{ s.label }}
                  </option>
                </select>
              </div>

              <div>
                <label class="block text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-1">Voto Personale (1–10)</label>
                <input
                  v-model.number="draft.score"
                  type="number"
                  min="1"
                  max="10"
                  inputmode="numeric"
                  class="w-full bg-white/5 border border-white/10 text-white text-xs rounded-xl p-2 focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all"
                />
              </div>

              <div>
                <label class="block text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-1">Gradimento</label>
                <select
                  v-model="draft.liked"
                  class="w-full bg-white/5 border border-white/10 text-white text-xs rounded-xl p-2 focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all [&>option]:bg-slate-950"
                >
                  <option :value="null">—</option>
                  <option
                    v-for="l in likedOptions"
                    :key="l.value"
                    :value="l.value"
                  >
                    {{ l.label }}
                  </option>
                </select>
              </div>

              <div>
                <label class="block text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-1">Nota</label>
                <textarea
                  v-model="draft.note"
                  rows="3"
                  class="w-full bg-white/5 border border-white/10 text-white text-xs rounded-xl p-2 focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all placeholder-gray-600"
                  placeholder="Aggiungi una nota personale..."
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Footer azioni -->
          <div class="pt-2 flex justify-end gap-2 border-t border-white/5">
            <button
              @click.stop="toggleEdit"
              type="button"
              class="px-3.5 py-1.5 text-xs font-semibold rounded-xl border border-white/10 text-gray-300 hover:bg-white/5 transition"
            >
              Annulla
            </button>
            <button
              @click.stop="save"
              :disabled="loading"
              type="button"
              class="px-3.5 py-1.5 text-xs font-semibold rounded-xl text-green-300 bg-green-500/10 border border-green-500/20 hover:bg-green-500/20 transition disabled:opacity-50"
            >
              Salva
            </button>
          </div>
        </div>
      </Transition>
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
});

const likedOptions = [
  { value: "loved", label: "Mi è piaciuto molto" },
  { value: "liked", label: "Mi è piaciuto" },
  { value: "okay", label: "Carino" },
  { value: "disliked", label: "Non mi è piaciuto" },
  { value: "terrible", label: "Pessimo" },
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

function toggleEdit() {
  editing.value = !editing.value;
  if (editing.value) {
    draft.status = props.movie.status;
    draft.score = props.movie.score;
    draft.liked = props.movie.liked;
    draft.note = props.movie.note;
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
  // normalizza score ('' -> null) e liked (stringa o null)
  const score =
    draft.score === "" || draft.score == null
      ? null
      : Math.max(1, Math.min(10, Number(draft.score)));

  const body = {
    status: draft.status,
    score: score ?? undefined, // undefined => non tocca il campo
    liked: draft.liked ?? undefined,
    note: (draft.note ?? "").trim() || undefined,
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
