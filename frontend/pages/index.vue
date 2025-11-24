<template>
  <div class="bg-white text-gray-900 font-sans">
    <!-- HERO SECTION -->
    <section class="relative overflow-hidden pt-32 pb-20 lg:pt-40 lg:pb-28">
      <!-- Background Gradients -->
      <div class="absolute inset-0 -z-10 pointer-events-none">
        <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full max-w-7xl">
          <div class="absolute top-20 left-10 w-72 h-72 bg-emerald-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
          <div class="absolute top-20 right-10 w-72 h-72 bg-sky-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
          <div class="absolute -bottom-32 left-1/2 -translate-x-1/2 w-72 h-72 bg-indigo-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
        </div>
      </div>

      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
        <!-- Badge -->
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-100 text-emerald-700 text-xs font-semibold uppercase tracking-wide mb-8">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          Nuovo • Beta Pubblica
        </div>

        <!-- Headline -->
        <h1 class="text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight text-gray-900 mb-6">
          La tua watchlist, <br class="hidden md:block" />
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-sky-600">finalmente ordinata.</span>
        </h1>

        <!-- Subheadline -->
        <p class="mt-4 max-w-2xl mx-auto text-xl text-gray-600 mb-10">
          PopCornNote unisce i tuoi film e serie preferiti in un'unica dashboard intelligente. 
          Cerca, salva, guarda e analizza le tue abitudini.
        </p>

        <!-- CTA Buttons -->
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
          <NuxtLink to="/register" class="w-full sm:w-auto px-8 py-4 rounded-2xl bg-gray-900 text-white font-semibold hover:bg-gray-800 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">
            Inizia gratis
          </NuxtLink>
          <NuxtLink to="/login" class="w-full sm:w-auto px-8 py-4 rounded-2xl bg-white border border-gray-200 text-gray-700 font-semibold hover:bg-gray-50 transition-all shadow-sm hover:shadow-md">
            Accedi
          </NuxtLink>
        </div>

        <!-- DASHBOARD MOCKUP (CSS Only) -->
        <div class="relative mx-auto max-w-5xl perspective-1000">
          <div class="relative rounded-2xl border border-gray-200 bg-white/50 backdrop-blur-xl shadow-2xl overflow-hidden transform rotate-x-12 transition-transform duration-700 hover:rotate-x-0">
            <!-- Mockup Header -->
            <div class="h-10 border-b border-gray-200 bg-gray-50/80 flex items-center px-4 gap-2">
              <div class="w-3 h-3 rounded-full bg-red-400"></div>
              <div class="w-3 h-3 rounded-full bg-amber-400"></div>
              <div class="w-3 h-3 rounded-full bg-emerald-400"></div>
              <div class="ml-4 w-64 h-5 bg-gray-200/50 rounded-md"></div>
            </div>
            
            <!-- Mockup Content -->
            <div class="p-6 grid grid-cols-12 gap-6 bg-white min-h-[400px]">
              <!-- Sidebar Mock -->
              <div class="hidden md:block col-span-3 space-y-4">
                <div class="h-8 w-3/4 bg-gray-100 rounded-lg"></div>
                <div class="space-y-2">
                  <div class="h-6 w-full bg-emerald-50 text-emerald-600 rounded-md flex items-center px-2 text-xs font-medium">Dashboard</div>
                  <div class="h-6 w-full hover:bg-gray-50 rounded-md"></div>
                  <div class="h-6 w-full hover:bg-gray-50 rounded-md"></div>
                </div>
              </div>

              <!-- Main Content Mock -->
              <div class="col-span-12 md:col-span-9">
                <!-- Greeting -->
                <div class="flex justify-between items-end mb-6">
                  <div>
                    <div class="h-4 w-32 bg-gray-100 rounded mb-2"></div>
                    <div class="h-8 w-64 bg-gradient-to-r from-emerald-600 to-sky-600 rounded-lg opacity-20"></div>
                  </div>
                  <div class="h-10 w-10 rounded-full bg-gray-100"></div>
                </div>

                <!-- Stats Grid -->
                <div class="grid grid-cols-3 gap-4 mb-8">
                  <div class="h-24 rounded-xl bg-emerald-50 border border-emerald-100 p-4">
                    <div class="h-8 w-8 rounded-full bg-emerald-200 mb-2"></div>
                    <div class="h-4 w-12 bg-emerald-200/50 rounded"></div>
                  </div>
                  <div class="h-24 rounded-xl bg-sky-50 border border-sky-100 p-4">
                    <div class="h-8 w-8 rounded-full bg-sky-200 mb-2"></div>
                    <div class="h-4 w-12 bg-sky-200/50 rounded"></div>
                  </div>
                  <div class="h-24 rounded-xl bg-indigo-50 border border-indigo-100 p-4">
                    <div class="h-8 w-8 rounded-full bg-indigo-200 mb-2"></div>
                    <div class="h-4 w-12 bg-indigo-200/50 rounded"></div>
                  </div>
                </div>

                <!-- Movie Cards -->
                <div class="grid grid-cols-3 gap-4">
                  <div class="aspect-[2/3] rounded-lg bg-gray-800 shadow-lg transform translate-y-2"></div>
                  <div class="aspect-[2/3] rounded-lg bg-gray-800 shadow-lg"></div>
                  <div class="aspect-[2/3] rounded-lg bg-gray-800 shadow-lg transform translate-y-4"></div>
                </div>
              </div>
            </div>
            
            <!-- Gradient Overlay -->
            <div class="absolute inset-0 bg-gradient-to-t from-white via-transparent to-transparent opacity-40"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- FEATURES SECTION -->
    <section class="py-24 bg-gray-50">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-3xl mx-auto mb-16">
          <h2 class="text-3xl font-bold text-gray-900 sm:text-4xl">Tutto quello che ti serve</h2>
          <p class="mt-4 text-lg text-gray-600">Un flusso lineare: cerca, salva, guarda, valuta. Con suggerimenti e statistiche a portata di click.</p>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <div class="group p-8 bg-white rounded-3xl border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
            <div class="w-12 h-12 bg-emerald-100 rounded-2xl flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform">
              📝
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">Watchlist Veloce</h3>
            <p class="text-gray-600 leading-relaxed">
              Aggiungi film e serie in un attimo. Organizza per stato (visto/da vedere) e tieni traccia di tutto ciò che ti interessa.
            </p>
          </div>

          <!-- Feature 2 -->
          <div class="group p-8 bg-white rounded-3xl border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
            <div class="w-12 h-12 bg-sky-100 rounded-2xl flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform">
              🔍
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">Ricerca TMDB</h3>
            <p class="text-gray-600 leading-relaxed">
              Integrazione diretta con TMDB. Trova locandine, trame, cast e voti senza mai uscire dall'applicazione.
            </p>
          </div>

          <!-- Feature 3 -->
          <div class="group p-8 bg-white rounded-3xl border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
            <div class="w-12 h-12 bg-indigo-100 rounded-2xl flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform">
              📊
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">Statistiche & KPI</h3>
            <p class="text-gray-600 leading-relaxed">
              Scopri i tuoi generi preferiti, quanto tempo passi a guardare serie TV e analizza le tue abitudini di visione.
            </p>
          </div>

          <!-- Feature 4 -->
          <div class="group p-8 bg-white rounded-3xl border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
            <div class="w-12 h-12 bg-amber-100 rounded-2xl flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform">
              🤝
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">Suggerimenti Smart</h3>
            <p class="text-gray-600 leading-relaxed">
              Non sai cosa guardare? Ricevi consigli basati su ciò che hai già visto e apprezzato.
            </p>
          </div>

          <!-- Feature 5 -->
          <div class="group p-8 bg-white rounded-3xl border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
            <div class="w-12 h-12 bg-rose-100 rounded-2xl flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform">
              ⬇️
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">Export CSV</h3>
            <p class="text-gray-600 leading-relaxed">
              I tuoi dati sono tuoi. Esporta l'intera libreria in formato CSV quando vuoi, per backup o analisi esterne.
            </p>
          </div>

          <!-- Feature 6 -->
          <div class="group p-8 bg-white rounded-3xl border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
            <div class="w-12 h-12 bg-gray-100 rounded-2xl flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform">
              ⚡
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">Performance Top</h3>
            <p class="text-gray-600 leading-relaxed">
              Costruito con Nuxt 3 e FastAPI. Un'esperienza utente fluida, veloce e reattiva su ogni dispositivo.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- STATS SECTION -->
    <section class="py-20 border-y border-gray-100">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10 text-center divide-y md:divide-y-0 md:divide-x divide-gray-100">
          <div class="p-4">
            <div class="text-4xl font-extrabold text-emerald-600 mb-2">30s</div>
            <div class="text-gray-500 font-medium">Per iniziare</div>
          </div>
          <div class="p-4">
            <div class="text-4xl font-extrabold text-sky-600 mb-2">∞</div>
            <div class="text-gray-500 font-medium">Titoli illimitati</div>
          </div>
          <div class="p-4">
            <div class="text-4xl font-extrabold text-indigo-600 mb-2">100%</div>
            <div class="text-gray-500 font-medium">Gratuito per sempre</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA SECTION -->
    <section class="py-24">
      <div class="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 text-center">
        <div class="bg-gray-900 rounded-[2.5rem] p-12 md:p-20 relative overflow-hidden">
          <!-- Decorative blobs -->
          <div class="absolute top-0 left-0 w-64 h-64 bg-emerald-500 rounded-full mix-blend-overlay filter blur-3xl opacity-20"></div>
          <div class="absolute bottom-0 right-0 w-64 h-64 bg-sky-500 rounded-full mix-blend-overlay filter blur-3xl opacity-20"></div>

          <h2 class="text-3xl md:text-4xl font-bold text-white mb-6 relative z-10">
            Pronto a mettere ordine nel caos?
          </h2>
          <p class="text-gray-300 text-lg mb-10 max-w-2xl mx-auto relative z-10">
            Unisciti agli altri appassionati di cinema e serie TV. Crea il tuo account gratuito in meno di un minuto.
          </p>
          <div class="flex flex-col sm:flex-row justify-center gap-4 relative z-10">
            <NuxtLink to="/register" class="px-8 py-4 rounded-xl bg-white text-gray-900 font-bold hover:bg-gray-100 transition-colors">
              Crea account gratuito
            </NuxtLink>
            <NuxtLink to="/login" class="px-8 py-4 rounded-xl border border-gray-700 text-white hover:bg-gray-800 transition-colors">
              Accedi
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.perspective-1000 {
  perspective: 1000px;
}

@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}
</style>


