import { defineNuxtConfig } from 'nuxt/config';
import tailwindcss from '@tailwindcss/vite';

export default defineNuxtConfig({
    modules: ['@nuxtjs/color-mode'],
  colorMode: {
    preference: 'system', // default theme
    fallback: 'dark', // fallback if system preference can't be detected
    classSuffix: '', // removes `-mode` suffix from class
  },
  compatibilityDate: '2025-07-01',
  css: [
    '~/assets/css/main.css'
  ],
  	vite: {
		plugins: [tailwindcss()],
	},
});
