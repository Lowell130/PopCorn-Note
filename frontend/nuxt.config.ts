// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000',
      // La chiave TMDb resta solo sul backend: il frontend non la espone più nel bundle.
      tmdbEnabled: process.env.NUXT_PUBLIC_TMDB_ENABLED !== 'false',
    }

  },
  app: {
    head: {
      title: 'PopCornNote',
      htmlAttrs: {
        lang: 'it'
      },
      meta: [
        { name: 'theme-color', content: '#020617' },
        { name: 'author', content: 'PopCornNote' },
        { name: 'description', content: 'PopCornNote — area riservata.' },
        // Il sito non deve comparire nei motori di ricerca
        { name: 'robots', content: 'noindex, nofollow, noarchive' },
        { name: 'googlebot', content: 'noindex, nofollow, noarchive' },
        { property: 'og:site_name', content: 'PopCornNote' },
        { property: 'og:type', content: 'website' },
        { property: 'og:locale', content: 'it_IT' },
        { property: 'og:title', content: 'PopCornNote' },
        { property: 'og:description', content: 'PopCornNote — area riservata.' },
        { property: 'og:image:width', content: '1200' },
        { property: 'og:image:height', content: '630' },
        { property: 'og:image', content: 'https://www.popcornote.com/og-image.jpg' },
        { name: 'twitter:card', content: 'summary_large_image' }
      ],
      link: [
        { rel: 'icon', type: 'image/png', href: '/favicon.png' },
        { rel: 'shortcut icon', href: '/favicon.ico' },
        { rel: 'apple-touch-icon', href: '/favicon.png' },
        // Font: preconnect + display=swap per non bloccare il rendering
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://image.tmdb.org', crossorigin: '' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap' }
      ]
    }
  },
  compatibilityDate: '2025-05-15',
  // devtools solo in sviluppo
  devtools: { enabled: process.env.NODE_ENV !== 'production' },
  ssr: false,
  routeRules: {
    '/': { prerender: true }
  },
  nitro: {
    prerender: {
      routes: ['/']
    }
  },
  css: ['~/assets/css/input.css'], // you'll have to create this file
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },

})
