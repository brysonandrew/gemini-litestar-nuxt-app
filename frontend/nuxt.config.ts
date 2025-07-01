import { defineNuxtConfig } from 'nuxt/config';
import tailwindcss from '@tailwindcss/vite';

export default defineNuxtConfig({
  modules: ['@tailwindcss/vite'],
  compatibilityDate: '2025-07-01',
  css: [
    '~/assets/css/main.css'
  ],
  	vite: {
		plugins: [tailwindcss()],
	},
});
