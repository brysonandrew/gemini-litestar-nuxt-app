import { defineNuxtConfig } from 'nuxt/config';

export default defineNuxtConfig({
  modules: ['@tailwindcss/vite'],
  compatibilityDate: '2025-07-01',
  css: [
    '~/assets/css/main.css'
  ]
});
