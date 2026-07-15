<template>
  <div class="text-white font-sans bg-transparent min-h-screen">
    <!-- HERO SECTION -->
    <section class="relative overflow-hidden pt-24 pb-20 lg:pt-36 lg:pb-28 px-4 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-7xl text-center">
        <!-- Floating Upper Badge -->
        <div class="inline-flex items-center gap-2.5 px-4 py-2 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-bold uppercase tracking-widest mb-8 backdrop-blur-md shadow-lg select-none">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-purple-500"></span>
          </span>
          🍿 La tua watchlist definitiva
        </div>

        <!-- Editorial Hero Title -->
        <h1 class="text-5xl sm:text-6xl lg:text-8xl font-black tracking-tight text-white mb-6 leading-tight max-w-5xl mx-auto">
          Tutto il tuo cinema. <br class="hidden sm:block" />
          In un unico, <span class="bg-gradient-to-r from-purple-400 via-pink-400 to-sky-400 bg-clip-text text-transparent">splendido posto.</span>
        </h1>

        <!-- Subheadline -->
        <p class="mt-6 max-w-3xl mx-auto text-lg sm:text-xl text-gray-300 mb-10 leading-relaxed">
          PopCornNote è l'organizzatore intelligente che unisce i tuoi film, le serie TV e le tue statistiche di visione. Veloce, open-source e gratuito per sempre.
        </p>

        <!-- CTA Buttons -->
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-20 max-w-md mx-auto sm:max-w-none">
          <NuxtLink to="/register" class="w-full sm:w-auto px-8 py-4 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/40 text-purple-200 font-bold rounded-2xl shadow-xl transition-all backdrop-blur-md text-center hover:scale-105 duration-200">
            Inizia gratis
          </NuxtLink>
          <NuxtLink to="/login" class="w-full sm:w-auto px-8 py-4 bg-white/5 border border-white/10 text-white rounded-2xl hover:bg-white/10 transition-all backdrop-blur-md text-center hover:scale-105 duration-200">
            Accedi
          </NuxtLink>
        </div>

        <!-- Floating Browser Mockup -->
        <div class="relative mx-auto max-w-5xl perspective-1000 animate-float">
          <div class="relative rounded-2xl border border-white/15 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden transform rotate-x-6 transition-all duration-700 hover:rotate-x-0 hover:scale-[1.01]">
            <!-- Mockup Header -->
            <div class="h-11 border-b border-white/10 bg-slate-950/90 flex items-center px-4 gap-2 select-none">
              <div class="w-3 h-3 rounded-full bg-rose-500/80"></div>
              <div class="w-3 h-3 rounded-full bg-amber-500/80"></div>
              <div class="w-3 h-3 rounded-full bg-emerald-500/80"></div>
              <div class="ml-4 w-48 sm:w-72 h-5 bg-white/5 rounded-md border border-white/5 flex items-center justify-center text-[10px] text-gray-500 font-mono tracking-wider">popcornnote.com/dashboard</div>
            </div>
            
            <!-- Mockup Content -->
            <div class="p-4 sm:p-6 grid grid-cols-12 gap-6 bg-slate-900/35 min-h-[420px] text-left">
              <!-- Sidebar Mock -->
              <div class="hidden md:block col-span-3 space-y-4 pr-4 border-r border-white/5">
                <div class="h-8 w-3/4 bg-white/5 rounded-lg border border-white/5"></div>
                <div class="space-y-2">
                  <div class="h-8 w-full bg-purple-500/10 text-purple-300 border border-purple-500/20 rounded-xl flex items-center px-3 text-xs font-semibold">🎬 Dashboard</div>
                  <div class="h-8 w-full hover:bg-white/5 rounded-xl border border-transparent"></div>
                  <div class="h-8 w-full hover:bg-white/5 rounded-xl border border-transparent"></div>
                </div>
              </div>

              <!-- Main Content Mock -->
              <div class="col-span-12 md:col-span-9 space-y-6">
                <!-- Greeting -->
                <div class="flex justify-between items-center">
                  <div>
                    <div class="h-4 w-28 bg-white/10 rounded mb-1"></div>
                    <div class="h-8 w-48 sm:w-64 bg-gradient-to-r from-purple-400 via-pink-400 to-sky-400 rounded-lg opacity-85"></div>
                  </div>
                  <div class="h-10 w-10 rounded-full bg-white/10 border border-white/10 flex items-center justify-center text-sm">👤</div>
                </div>

                <!-- Action Bar -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div class="h-12 bg-purple-500/10 border border-purple-500/20 text-purple-300 rounded-xl flex items-center px-4 text-xs font-semibold select-none gap-2">
                    <span>🎬</span> Aggiungi Film o Serie TV
                  </div>
                  <div class="h-12 bg-white/5 border border-white/10 text-white/80 rounded-xl flex items-center px-4 text-xs font-semibold select-none gap-2">
                    <span>🎲</span> Fai scegliere al fato
                  </div>
                </div>

                <!-- Stats Grid -->
                <div class="grid grid-cols-3 gap-4">
                  <div class="h-20 sm:h-24 rounded-2xl bg-white/5 border border-white/10 p-4">
                    <div class="h-3 w-12 bg-gray-400 rounded mb-2"></div>
                    <div class="h-7 w-8 bg-white/10 rounded"></div>
                  </div>
                  <div class="h-20 sm:h-24 rounded-2xl bg-white/5 border border-white/10 p-4">
                    <div class="h-3 w-12 bg-gray-400 rounded mb-2"></div>
                    <div class="h-7 w-8 bg-white/10 rounded"></div>
                  </div>
                  <div class="h-20 sm:h-24 rounded-2xl bg-white/5 border border-white/10 p-4">
                    <div class="h-3 w-12 bg-gray-400 rounded mb-2"></div>
                    <div class="h-7 w-8 bg-white/10 rounded"></div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Bottom Fading Glow -->
            <div class="absolute inset-x-0 bottom-0 h-20 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent pointer-events-none"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- LIVE INTERACTIVE PLAYGROUND (Chiedi al Fato) -->
    <section class="py-24 bg-black/30 border-y border-white/5 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      <!-- Background Spotlight -->
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full bg-purple-500/5 blur-3xl pointer-events-none"></div>

      <div class="mx-auto max-w-5xl">
        <div class="bg-white/5 border border-white/10 rounded-3xl p-8 sm:p-12 backdrop-blur-md shadow-2xl relative">
          <div class="grid md:grid-cols-12 gap-10 items-center">
            
            <!-- Left Info -->
            <div class="md:col-span-7 space-y-6 text-left">
              <div class="inline-block px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-bold uppercase tracking-wider">Playground Interattivo</div>
              <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">Troppo indeciso stasera? <br />Lascia fare al Fato.</h2>
              <p class="text-gray-300 leading-relaxed text-sm sm:text-base">
                La stanchezza da catalogo è reale. PopCornNote risolve i dubbi con un estrattore casuale intelligente integrato. Prova a cliccare il pulsante qui sotto per vedere come funziona in tempo reale direttamente sulla nostra landing page!
              </p>
              
              <button 
                @click="rollFato" 
                :disabled="isRolling"
                class="inline-flex items-center gap-3 px-6 py-4 bg-purple-500/20 hover:bg-purple-500/30 disabled:bg-purple-500/5 border border-purple-500/40 text-purple-300 font-bold rounded-2xl transition-all transform hover:scale-102 active:scale-98 disabled:opacity-50 disabled:cursor-not-allowed select-none shadow-lg shadow-purple-500/5"
              >
                <span>🎲</span>
                <span>{{ isRolling ? 'Il Fato sta decidendo...' : 'Fai scegliere al Fato' }}</span>
              </button>
            </div>

            <!-- Right Terminal / Visual Screen -->
            <div class="md:col-span-5 w-full">
              <div class="bg-slate-950/80 border border-white/10 rounded-2xl p-6 min-h-[180px] flex flex-col justify-center items-center text-center relative overflow-hidden shadow-2xl">
                <!-- Floating corner lights -->
                <div class="absolute -top-10 -right-10 w-24 h-24 rounded-full bg-purple-500/10 blur-xl"></div>
                
                <!-- Rotating Title -->
                <Transition name="fade-bounce" mode="out-in">
                  <div :key="selectedMovie" class="space-y-3">
                    <span class="text-[10px] uppercase font-bold text-gray-500 tracking-widest block">Estrazione Casuale</span>
                    
                    <h3 
                      :class="[
                        'text-xl sm:text-2xl font-black tracking-tight leading-tight px-4 transition-all duration-300',
                        isRolling ? 'text-gray-400 scale-95 opacity-80' : 'text-purple-300 scale-100 glow-text'
                      ]"
                    >
                      "{{ selectedMovie }}"
                    </h3>

                    <!-- Success Tag -->
                    <div 
                      v-if="rollResult" 
                      class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-[10px] font-bold uppercase tracking-wider animate-pulse-fast mx-auto"
                    >
                      <span>✨</span> Scelta Perfetta
                    </div>
                  </div>
                </Transition>
              </div>
            </div>

          </div>
        </div>
      </div>
    </section>

    <!-- ALTERNATING STORY SHOWCASE SECTION -->
    <section class="py-24 space-y-32 px-4 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-7xl">
        
        <!-- Story 1: Dashboard & TMDb -->
        <div class="grid md:grid-cols-12 gap-12 items-center">
          <!-- Text -->
          <div class="md:col-span-6 space-y-6 text-left">
            <div class="w-12 h-12 rounded-2xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center">
              <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
              </svg>
            </div>
            <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">Sincronizzazione TMDb istantanea.</h2>
            <p class="text-gray-300 leading-relaxed text-base">
              Non inserire dati a mano. Cerca qualsiasi titolo e PopCornNote importerà automaticamente copertine ad alta risoluzione, trama ufficiale, trailer, generi e punteggi del database ufficiale TMDb.
            </p>
            <ul class="space-y-2 text-sm text-gray-400">
              <li class="flex items-center gap-2">✔ Metadati completi all'istante</li>
              <li class="flex items-center gap-2">✔ Cast, registi e troupe organizzati</li>
              <li class="flex items-center gap-2">✔ Aggiornamento automatico dei voti</li>
            </ul>
          </div>
          <!-- Visual Mockup -->
          <div class="md:col-span-6 w-full">
            <div class="bg-white/5 border border-white/10 rounded-3xl p-6 backdrop-blur-md shadow-2xl relative overflow-hidden">
              <div class="absolute -top-20 -right-20 w-48 h-48 rounded-full bg-purple-500/5 blur-3xl"></div>
              <!-- Mock Movie Info Card -->
              <div class="space-y-4">
                <div class="h-44 rounded-xl bg-slate-950/40 border border-white/5 relative overflow-hidden flex items-end p-4">
                  <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/20 to-transparent z-10"></div>
                  <div class="relative z-20 space-y-1">
                    <span class="px-2 py-0.5 rounded bg-purple-500/20 border border-purple-500/30 text-purple-300 text-[9px] font-bold uppercase tracking-wider">Fantascienza</span>
                    <h4 class="text-lg font-bold text-white leading-tight">Interstellar</h4>
                  </div>
                </div>
                <p class="text-xs text-gray-400 text-left leading-relaxed">
                  Un gruppo di esploratori intraprende il viaggio più importante della storia dell'umanità: superare i confini della nostra galassia per scoprire se l'uomo ha un futuro tra le stelle.
                </p>
                <div class="flex justify-between items-center text-xs pt-2 border-t border-white/5">
                  <span class="text-amber-400 font-semibold flex items-center gap-1">⭐ 8.4/10 <span class="text-gray-500 text-[10px]">(TMDb)</span></span>
                  <span class="text-gray-500">Regia: Christopher Nolan</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Story 2: Analytics (Text left on mobile, right on desktop) -->
        <div class="grid md:grid-cols-12 gap-12 items-center pt-32">
          <!-- Visual Mockup (First on Desktop) -->
          <div class="md:col-span-6 w-full order-last md:order-first">
            <div class="bg-white/5 border border-white/10 rounded-3xl p-6 backdrop-blur-md shadow-2xl relative overflow-hidden">
              <!-- Simulated charts -->
              <div class="space-y-6 text-left">
                <h4 class="text-sm font-bold text-white flex items-center gap-2 select-none">📊 Statistiche Generi</h4>
                <div class="space-y-3">
                  <div>
                    <div class="flex justify-between text-xs mb-1">
                      <span class="text-gray-400">Sci-Fi & Fantasy</span>
                      <span class="text-white font-semibold">58%</span>
                    </div>
                    <div class="h-2 bg-white/10 rounded-full overflow-hidden">
                      <div class="h-full bg-purple-500 rounded-full" style="width: 58%"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between text-xs mb-1">
                      <span class="text-gray-400">Drammatico</span>
                      <span class="text-white font-semibold">42%</span>
                    </div>
                    <div class="h-2 bg-white/10 rounded-full overflow-hidden">
                      <div class="h-full bg-sky-500 rounded-full" style="width: 42%"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between text-xs mb-1">
                      <span class="text-gray-400">Thriller</span>
                      <span class="text-white font-semibold">25%</span>
                    </div>
                    <div class="h-2 bg-white/10 rounded-full overflow-hidden">
                      <div class="h-full bg-emerald-500 rounded-full" style="width: 25%"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Text -->
          <div class="md:col-span-6 space-y-6 text-left">
            <div class="w-12 h-12 rounded-2xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center">
              <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M7 12l3-3 3 3 4-4M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
            <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">Conosci la tua passione.</h2>
            <p class="text-gray-300 leading-relaxed text-base">
              Esplora report grafici avanzati sulle tue abitudini di visione. Scopri i tuoi generi preferiti, traccia la timeline temporale dei film per decenni e monitora l'evoluzione dei tuoi voti personali.
            </p>
            <ul class="space-y-2 text-sm text-gray-400">
              <li class="flex items-center gap-2">✔ Grafici a barre su registi e decenni</li>
              <li class="flex items-center gap-2">✔ Analisi sul tempo trascorso a guardare serie TV</li>
              <li class="flex items-center gap-2">✔ Curva di frequenza delle votazioni</li>
            </ul>
          </div>
        </div>

        <!-- Story 3: Community -->
        <div class="grid md:grid-cols-12 gap-12 items-center pt-32">
          <!-- Text -->
          <div class="md:col-span-6 space-y-6 text-left">
            <div class="w-12 h-12 rounded-2xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center">
              <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">Connettiti con altri cinefili.</h2>
            <p class="text-gray-300 leading-relaxed text-base">
              Non guardare film in solitudine. Condividi recensioni e opinioni calde sul feed community, commenta i titoli con gli amici e reagisci alle attività altrui in tempo reale.
            </p>
            <ul class="space-y-2 text-sm text-gray-400">
              <li class="flex items-center gap-2">✔ Feed social integrato e pulito</li>
              <li class="flex items-center gap-2">✔ Condivisione recensioni in un click</li>
              <li class="flex items-center gap-2">✔ Reazioni immediate (cuori e mi piace)</li>
            </ul>
          </div>
          <!-- Visual Mockup -->
          <div class="md:col-span-6 w-full">
            <div class="bg-white/5 border border-white/10 rounded-3xl p-6 backdrop-blur-md shadow-2xl relative overflow-hidden">
              <!-- Mock Social Post -->
              <div class="space-y-4 text-left text-xs">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-purple-500/20 border border-purple-500/30 flex items-center justify-center font-bold text-purple-300 text-xs">A</div>
                  <div>
                    <h5 class="font-bold text-white">Alice R.</h5>
                    <span class="text-gray-500 text-[10px]">2 ore fa</span>
                  </div>
                </div>
                <p class="text-gray-300 leading-relaxed text-xs">
                  Ho appena finito *Dune - Parte Due* al cinema. La colonna sonora di Hans Zimmer ed il design visivo sono indescrivibili. Assolutamente da vedere in sala! 🎬✨
                </p>
                <div class="flex items-center gap-4 text-gray-500 pt-2 border-t border-white/5">
                  <span class="hover:text-purple-400 transition cursor-pointer">❤️ 18 Reazioni</span>
                  <span class="hover:text-purple-400 transition cursor-pointer">💬 3 Commenti</span>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- METRICS SECTION -->
    <section class="py-20 border-y border-white/10 px-4 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-7xl">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10 text-center divide-y md:divide-y-0 md:divide-x divide-white/10">
          <div class="p-4">
            <div class="text-4xl font-extrabold text-purple-400 mb-2">30s</div>
            <div class="text-gray-400 font-semibold text-sm tracking-widest uppercase">Tempo di setup</div>
          </div>
          <div class="p-4">
            <div class="text-4xl font-extrabold text-sky-400 mb-2">∞</div>
            <div class="text-gray-400 font-semibold text-sm tracking-widest uppercase">Titoli inseribili</div>
          </div>
          <div class="p-4">
            <div class="text-4xl font-extrabold text-emerald-400 mb-2">100%</div>
            <div class="text-gray-400 font-semibold text-sm tracking-widest uppercase">Gratuito e open-source</div>
          </div>
        </div>
      </div>
    </section>

    <!-- FINAL CTA SECTION -->
    <section class="py-28 px-4 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-5xl text-center">
        <div class="bg-slate-950/50 border border-white/10 rounded-[2.5rem] p-12 md:p-20 relative overflow-hidden backdrop-blur-md shadow-2xl">
          <!-- Decorative ambient glows -->
          <div class="absolute top-0 left-0 w-64 h-64 bg-purple-500/10 rounded-full mix-blend-overlay filter blur-3xl opacity-20 pointer-events-none"></div>
          <div class="absolute bottom-0 right-0 w-64 h-64 bg-sky-500/10 rounded-full mix-blend-overlay filter blur-3xl opacity-20 pointer-events-none"></div>

          <h2 class="text-4xl md:text-6xl font-black text-white mb-6 relative z-10 tracking-tight leading-tight">
            Pronto a ordinare <br />le tue visioni?
          </h2>
          <p class="text-gray-300 text-lg mb-10 max-w-2xl mx-auto relative z-10 leading-relaxed">
            Unisciti a centinaia di cinefili. Crea la tua watchlist centralizzata e gratuita in meno di un minuto.
          </p>
          <div class="flex flex-col sm:flex-row justify-center gap-4 relative z-10 max-w-xs sm:max-w-none mx-auto">
            <NuxtLink to="/register" class="px-8 py-4 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/40 text-purple-200 font-bold rounded-2xl shadow-xl transition-all backdrop-blur-md text-center hover:scale-105 duration-200">
              Crea account gratuito
            </NuxtLink>
            <NuxtLink to="/login" class="px-8 py-4 bg-white/5 border border-white/10 text-white rounded-2xl hover:bg-white/10 transition-all backdrop-blur-md text-center hover:scale-105 duration-200">
              Accedi
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'landing'
})

// Simulated movies for the "Fai scegliere al Fato" playground widget
const moviePool = [
  'Inception',
  'Pulp Fiction',
  'Interstellar',
  'Parasite',
  'The Matrix',
  'Fight Club',
  'La Città Incantata',
  'Whiplash',
  'Il Cavaliere Oscuro',
  'Il Gladiatore',
  'Django Unchained',
  'Spider-Man: Un nuovo universo'
]

const selectedMovie = ref('Quale film guarderai stasera?')
const isRolling = ref(false)
const rollResult = ref(null)

function rollFato() {
  if (isRolling.value) return
  isRolling.value = true
  rollResult.value = null
  
  let count = 0
  const maxCycles = 16
  const interval = setInterval(() => {
    // Pick random title rapidly
    const randomIndex = Math.floor(Math.random() * moviePool.length)
    selectedMovie.value = moviePool[randomIndex]
    count++
    
    if (count >= maxCycles) {
      clearInterval(interval)
      // Pick final random selection
      const finalIndex = Math.floor(Math.random() * moviePool.length)
      selectedMovie.value = moviePool[finalIndex]
      rollResult.value = selectedMovie.value
      isRolling.value = false
    }
  }, 70)
}

// Advanced SEO Metadata
useSeoMeta({
  title: 'PopCornNote - Watchlist Intelligente per Film e Serie TV',
  ogTitle: 'PopCornNote - Watchlist Intelligente di Film e Serie TV',
  description: 'Organizza la tua collezione di film e serie TV con PopCornNote. Cerca con TMDb, visualizza statistiche avanzate, condividi con la community ed esporta i tuoi dati in CSV.',
  ogDescription: 'Watchlist intelligente e gratuita per gli amanti del cinema. Ottieni statistiche avanzate, consigli e condividi le tue opinioni.',
  ogImage: '/logo.png',
  ogType: 'website',
  twitterCard: 'summary_large_image',
  robots: 'index, follow',
  keywords: 'watchlist film, tracciare serie tv, database film personale, statistiche film, tmdb italiano, community cinema, popcornnote'
})

// Canonical link & Schema.org JSON-LD Structured Data
useHead({
  htmlAttrs: {
    lang: 'it'
  },
  link: [
    { rel: 'canonical', href: 'https://popcornnote.com' }
  ],
  script: [
    {
      type: 'application/ld+json',
      children: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "PopCornNote",
        "operatingSystem": "All",
        "applicationCategory": "EntertainmentApplication",
        "offers": {
          "@type": "Offer",
          "price": "0",
          "priceCurrency": "EUR"
        },
        "description": "Watchlist intelligente e gratuita per organizzare film e serie TV con statistiche avanzate e integrazione TMDb.",
        "aggregateRating": {
          "@type": "AggregateRating",
          "ratingValue": "4.8",
          "ratingCount": "150"
        }
      })
    }
  ]
})
</script>

<style scoped>
.perspective-1000 {
  perspective: 1000px;
}

/* Glow styling for text */
.glow-text {
  text-shadow: 0 0 12px rgba(168, 85, 247, 0.4);
}

/* Transitions for Playground */
.fade-bounce-enter-active {
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.fade-bounce-leave-active {
  transition: all 0.15s ease-in;
}
.fade-bounce-enter-from {
  opacity: 0;
  transform: scale(0.9) translateY(5px);
}
.fade-bounce-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-5px);
}

/* Pulsing fast animation */
@keyframes pulse-fast {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.85; transform: scale(1.03); }
}
.animate-pulse-fast {
  animation: pulse-fast 1.5s infinite ease-in-out;
}

/* Hero browser float keyframes */
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-12px); }
}
.animate-float {
  animation: float 6s infinite ease-in-out;
}
</style>
