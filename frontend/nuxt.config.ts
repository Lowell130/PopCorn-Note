// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://127.0.0.1:8000",
      tmdbApiKey: process.env.NUXT_PUBLIC_TMDB_API_KEY || "",
    },
  },

  app: {
    head: {
      title: "PopCornNote",
      link: [
        { rel: "preconnect", href: "https://fonts.googleapis.com" },
        { rel: "preconnect", href: "https://fonts.gstatic.com", crossorigin: "" },
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        },
      ],
    },
  },

  compatibilityDate: "2025-05-15",
  devtools: { enabled: true },
  ssr: false,

  css: ["~/assets/css/input.css"],

  modules: [
    "@vite-pwa/nuxt",
  ],

  pwa: {
    registerType: "autoUpdate",
    manifest: {
      name: "PopCornNote",
      short_name: "PopCornNote",
      description: "La tua libreria personale di film e serie TV",
      theme_color: "#111827",
      background_color: "#111827",
      display: "standalone",
      orientation: "portrait-primary",
      start_url: "/",
      icons: [
        { src: "/pwa-192x192.png", sizes: "192x192", type: "image/png" },
        { src: "/pwa-512x512.png", sizes: "512x512", type: "image/png" },
        {
          src: "/pwa-512x512-maskable.png",
          sizes: "512x512",
          type: "image/png",
          purpose: "maskable",
        },
      ],
    },
    workbox: {
      globPatterns: ["**/*.{js,css,html,ico,png,svg}"],
        // Evita warning in dev
    globDirectory: "."
    },
    client: {
      installPrompt: true,
    },
    devOptions: {
      enabled: true,   // 👈 PWA attivo anche in dev
      type: "module",
    },
  },

  vite: {
    plugins: [tailwindcss()],
  },
});


