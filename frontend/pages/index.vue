<template>
  <div class="bg-white text-gray-900">
    <!-- HERO -->
    <section class="relative overflow-hidden">
      <div class="absolute inset-0 -z-10">
        <div class="absolute -top-24 -right-24 h-72 w-72 rounded-full bg-blue-100 blur-3xl opacity-60"></div>
        <div class="absolute -bottom-24 -left-24 h-72 w-72 rounded-full bg-indigo-100 blur-3xl opacity-60"></div>
      </div>

      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-24 pb-16 grid lg:grid-cols-12 gap-10 items-center">
        <!-- Copy -->
        <div class="lg:col-span-7">
          <span class="inline-flex items-center gap-2 text-xs font-semibold tracking-wider uppercase text-blue-700 bg-blue-100 rounded-full px-3 py-1">
            <span class="h-2 w-2 rounded-full bg-blue-600"></span>
            Nuovo • Beta pubblica
          </span>

          <h1 class="mt-4 text-4xl sm:text-5xl font-extrabold leading-tight">
            Tieni traccia di <span class="text-blue-600">film e serie</span>, scopri nuovi titoli e monitora le tue abitudini in modo <span class="underline decoration-indigo-400 decoration-4 underline-offset-4">semplice</span>.
          </h1>

          <p class="mt-6 text-lg text-gray-600 max-w-2xl">
            PopCornNote unisce watchlist, suggerimenti intelligenti da TMDB e una dashboard personale con statistiche e KPI. Minimal, veloce, pensato per chi guarda davvero.
          </p>

          <div class="mt-8 flex flex-wrap gap-3">
            <NuxtLink to="/register" class="px-5 py-3 rounded-xl bg-blue-600 text-white hover:bg-blue-700 shadow-sm">
              Inizia gratis
            </NuxtLink>
            <NuxtLink to="/login" class="px-5 py-3 rounded-xl border border-gray-300 hover:bg-gray-50">
              Accedi
            </NuxtLink>
            <NuxtLink to="/news" class="px-5 py-3 rounded-xl border border-transparent hover:bg-gray-50">
              Novità prodotto
            </NuxtLink>
          </div>

          <p class="mt-4 text-sm text-gray-500">
            Nessuna carta richiesta. Disdici quando vuoi. Export CSV sempre disponibile.
          </p>

          <!-- Trust bar -->
          <div class="mt-8 flex flex-wrap items-center gap-6 text-xs text-gray-500">
            <div class="flex items-center gap-2">
              <span class="i">🔒</span> Login sicuro con JWT
            </div>
            <div class="flex items-center gap-2">
              <span class="i">⚡</span> Super veloce (Nuxt 3 + FastAPI)
            </div>
            <div class="flex items-center gap-2">
              <span class="i">📈</span> KPI personali
            </div>
          </div>
        </div>

        <!-- Visual -->
        <div class="lg:col-span-5">
          <div class="relative">
            <div class="absolute -inset-4 -z-10 rounded-3xl bg-gradient-to-tr from-blue-100 via-indigo-100 to-purple-100 blur-2xl"></div>
            <div class="rounded-3xl border border-gray-200 overflow-hidden shadow-xl bg-gray-50 aspect-[16/10] flex items-center justify-center">
              <!-- Placeholder immagine/screenshot -->
              <div class="text-gray-400 text-sm">Anteprima dashboard / mockup</div>
            </div>
            <div class="absolute -bottom-6 -left-6 rounded-2xl border bg-white p-4 shadow-md hidden md:flex items-center gap-3">
              <span class="text-2xl">🍿</span>
              <div>
                <p class="font-semibold text-sm">Aggiungi alla watchlist</p>
                <p class="text-xs text-gray-500">Un click da TMDB alla tua lista</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FEATURE GRID -->
    <section class="py-16">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-2xl mx-auto">
          <h2 class="text-3xl font-bold">Tutto quello che ti serve</h2>
          <p class="mt-3 text-gray-600">Un flusso lineare: cerca, salva, guarda, valuta. Con suggerimenti e statistiche a portata di click.</p>
        </div>

        <div class="mt-10 grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div class="p-6 rounded-2xl border bg-white">
            <div class="text-2xl">📝</div>
            <h3 class="mt-3 font-semibold">Watchlist veloce</h3>
            <p class="mt-2 text-sm text-gray-600">Aggiungi film e serie in un attimo, organizza per stato (visto/da vedere) e rating personale.</p>
          </div>
          <div class="p-6 rounded-2xl border bg-white">
            <div class="text-2xl">🔍</div>
            <h3 class="mt-3 font-semibold">Ricerca TMDB</h3>
            <p class="mt-2 text-sm text-gray-600">Integra TMDB per trovare titoli e leggere le info principali senza uscire dall’app.</p>
          </div>
          <div class="p-6 rounded-2xl border bg-white">
            <div class="text-2xl">🤝</div>
            <h3 class="mt-3 font-semibold">Correlati intelligenti</h3>
            <p class="mt-2 text-sm text-gray-600">Scopri contenuti simili ai tuoi gusti, con suggerimenti basati sui tuoi salvataggi.</p>
          </div>
          <div class="p-6 rounded-2xl border bg-white">
            <div class="text-2xl">📊</div>
            <h3 class="mt-3 font-semibold">KPI & Statistiche</h3>
            <p class="mt-2 text-sm text-gray-600">Dashboard personale con abitudini di visione, generi preferiti e trend settimanali.</p>
          </div>
          <div class="p-6 rounded-2xl border bg-white">
            <div class="text-2xl">⬇️</div>
            <h3 class="mt-3 font-semibold">Export & Privacy</h3>
            <p class="mt-2 text-sm text-gray-600">Esporta i tuoi dati in CSV quando vuoi. I dati sono tuoi, per sempre.</p>
          </div>
          <div class="p-6 rounded-2xl border bg-white">
            <div class="text-2xl">⚙️</div>
            <h3 class="mt-3 font-semibold">Semplice ma potente</h3>
            <p class="mt-2 text-sm text-gray-600">UI minimale, prestazioni alte. Niente fronzoli, solo ciò che serve davvero.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- HOW IT WORKS -->
    <section class="py-16 bg-gray-50">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="grid lg:grid-cols-3 gap-8 items-start">
          <div>
            <h2 class="text-3xl font-bold">Come funziona</h2>
            <p class="mt-3 text-gray-600">Dalla ricerca alla valutazione, tutto in 3 passaggi chiari.</p>
            <div class="mt-6 flex gap-3">
              <NuxtLink to="/register" class="px-5 py-3 rounded-xl bg-blue-600 text-white hover:bg-blue-700 shadow-sm">Crea un account</NuxtLink>
              <NuxtLink to="/login" class="px-5 py-3 rounded-xl border hover:bg-gray-100">Prova ora</NuxtLink>
            </div>
          </div>
          <div class="lg:col-span-2 grid sm:grid-cols-3 gap-6">
            <div class="p-6 rounded-2xl border bg-white">
              <div class="text-xl">1️⃣</div>
              <h3 class="mt-3 font-semibold">Cerca e salva</h3>
              <p class="mt-2 text-sm text-gray-600">Trova titoli da TMDB e aggiungili alla tua watchlist con un click.</p>
            </div>
            <div class="p-6 rounded-2xl border bg-white">
              <div class="text-xl">2️⃣</div>
              <h3 class="mt-3 font-semibold">Guarda e valuta</h3>
              <p class="mt-2 text-sm text-gray-600">Segna ciò che hai visto e assegna un voto. Mantieni la cronologia aggiornata.</p>
            </div>
            <div class="p-6 rounded-2xl border bg-white">
              <div class="text-xl">3️⃣</div>
              <h3 class="mt-3 font-semibold">Analizza e scopri</h3>
              <p class="mt-2 text-sm text-gray-600">Statistiche, generi top e suggerimenti correlati per decidere cosa vedere dopo.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- STATS / SOCIAL PROOF -->
    <section class="py-16">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="grid md:grid-cols-3 gap-6">
          <div class="p-6 rounded-2xl border bg-white text-center">
            <div class="text-3xl font-extrabold">30s</div>
            <p class="mt-1 text-sm text-gray-600">per creare la tua prima watchlist</p>
          </div>
          <div class="p-6 rounded-2xl border bg-white text-center">
            <div class="text-3xl font-extrabold">∞</div>
            <p class="mt-1 text-sm text-gray-600">titoli: nessun limite artificiale</p>
          </div>
          <div class="p-6 rounded-2xl border bg-white text-center">
            <div class="text-3xl font-extrabold">100%</div>
            <p class="mt-1 text-sm text-gray-600">export sempre disponibile</p>
          </div>
        </div>
      </div>
    </section>

    <!-- TESTIMONIALS -->
    <section class="py-16 bg-gray-50">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-2xl mx-auto">
          <h2 class="text-3xl font-bold">Cosa dicono gli utenti</h2>
          <p class="mt-3 text-gray-600">Semplicità, velocità e zero distrazioni.</p>
        </div>
        <div class="mt-10 grid md:grid-cols-3 gap-6">
          <div class="p-6 rounded-2xl border bg-white">
            <p class="text-sm text-gray-700">“Finalmente un tracker che non mi fa perdere tempo. Aggiungo da TMDB e ho finito.”</p>
            <div class="mt-4 flex items-center gap-3">
              <div class="h-10 w-10 rounded-full bg-gray-200"></div>
              <div>
                <div class="text-sm font-semibold">Luca</div>
                <div class="text-xs text-gray-500">Appassionato di cinema</div>
              </div>
            </div>
          </div>
          <div class="p-6 rounded-2xl border bg-white">
            <p class="text-sm text-gray-700">“Le statistiche mi aiutano a scegliere cosa vedere. Interfaccia pulita e intuitiva.”</p>
            <div class="mt-4 flex items-center gap-3">
              <div class="h-10 w-10 rounded-full bg-gray-200"></div>
              <div>
                <div class="text-sm font-semibold">Giulia</div>
                <div class="text-xs text-gray-500">Serie-addicted</div>
              </div>
            </div>
          </div>
          <div class="p-6 rounded-2xl border bg-white">
            <p class="text-sm text-gray-700">“Export CSV e via: perfetto per i miei riepiloghi mensili. Bravi.”</p>
            <div class="mt-4 flex items-center gap-3">
              <div class="h-10 w-10 rounded-full bg-gray-200"></div>
              <div>
                <div class="text-sm font-semibold">Marco</div>
                <div class="text-xs text-gray-500">Data nerd</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- PRICING / CTA -->
    <section class="py-16">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="grid lg:grid-cols-3 gap-8 items-stretch">
          <div class="lg:col-span-2">
            <h2 class="text-3xl font-bold">Prezzo trasparente</h2>
            <p class="mt-3 text-gray-600">Inizia gratis, poi resta su free o passa al piano Pro quando ti serve di più.</p>

            <div class="mt-6 grid sm:grid-cols-2 gap-6">
              <div class="p-6 rounded-2xl border bg-white">
                <div class="flex items-baseline gap-2">
                  <div class="text-3xl font-extrabold">Free</div>
                  <div class="text-sm text-gray-500">/ per sempre</div>
                </div>
                <ul class="mt-4 space-y-2 text-sm text-gray-700">
                  <li>• Watchlist illimitata</li>
                  <li>• Ricerca TMDB</li>
                  <li>• Export CSV</li>
                </ul>
                <NuxtLink to="/register" class="mt-6 inline-flex px-4 py-2 rounded-xl bg-gray-900 text-white hover:bg-black">Crea account</NuxtLink>
              </div>

              <div class="p-6 rounded-2xl border bg-white">
                <div class="flex items-baseline gap-2">
                  <div class="text-3xl font-extrabold">Pro</div>
                  <div class="text-sm text-gray-500">/ mese</div>
                </div>
                <ul class="mt-4 space-y-2 text-sm text-gray-700">
                  <li>• Tutto del Free</li>
                  <li>• Statistiche avanzate</li>
                  <li>• Backup automatici</li>
                  <li>• Supporto prioritario</li>
                </ul>
                <NuxtLink to="/register" class="mt-6 inline-flex px-4 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700">Prova gratis</NuxtLink>
              </div>
            </div>
          </div>

          <div class="p-6 rounded-2xl border bg-white">
            <h3 class="font-semibold">Domande frequenti</h3>
            <div class="mt-4 space-y-4">
              <details class="group p-4 rounded-lg border">
                <summary class="flex justify-between items-center cursor-pointer list-none">
                  <span class="font-medium">Posso esportare i miei dati?</span>
                  <span class="transition group-open:rotate-180">⌄</span>
                </summary>
                <p class="mt-2 text-sm text-gray-600">Sì, in qualsiasi momento, in formato CSV.</p>
              </details>
              <details class="group p-4 rounded-lg border">
                <summary class="flex justify-between items-center cursor-pointer list-none">
                  <span class="font-medium">Serve la carta di credito?</span>
                  <span class="transition group-open:rotate-180">⌄</span>
                </summary>
                <p class="mt-2 text-sm text-gray-600">No, per iniziare basta l’email. La carta è richiesta solo per il Pro.</p>
              </details>
              <details class="group p-4 rounded-lg border">
                <summary class="flex justify-between items-center cursor-pointer list-none">
                  <span class="font-medium">Posso usare le preview TMDB?</span>
                  <span class="transition group-open:rotate-180">⌄</span>
                </summary>
                <p class="mt-2 text-sm text-gray-600">Certo, PopCornNote integra TMDB per darti info essenziali sui titoli.</p>
              </details>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FINAL CTA -->
    <section class="py-16 bg-gray-50">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl font-bold">Pronto a mettere ordine nella tua watchlist?</h2>
        <p class="mt-3 text-gray-600">Crea un account in meno di un minuto. Gratis. Sempre tuo.</p>
        <div class="mt-6 flex justify-center gap-3">
          <NuxtLink to="/register" class="px-6 py-3 rounded-xl bg-blue-600 text-white hover:bg-blue-700">Inizia gratis</NuxtLink>
          <NuxtLink to="/login" class="px-6 py-3 rounded-xl border hover:bg-gray-100">Accedi</NuxtLink>
        </div>
      </div>
    </section>
  </div>
</template>

