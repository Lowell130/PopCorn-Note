// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000',

      tmdbApiKey: process.env.NUXT_PUBLIC_TMDB_API_KEY || ''
    }

  },
  app: {
    head: {
      title: 'PopCornNote - Watchlist Intelligente per Film e Serie TV',
      htmlAttrs: {
        lang: 'it'
      },
      meta: [
        { name: 'theme-color', content: '#020617' },
        { name: 'author', content: 'PopCornNote' }
      ],
      link: [
        { rel: 'icon', type: 'image/png', href: '/favicon.png' },
        { rel: 'shortcut icon', href: '/favicon.ico' },
        { rel: 'apple-touch-icon', href: '/favicon.png' },
        // Font opzionale
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap' }
      ]
    }
  },
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
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
