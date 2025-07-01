<script setup>
import { ref, onMounted } from 'vue'

const isDarkMode = ref(false)

onMounted(() => {
  // Check local storage for theme preference
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDarkMode.value = true
    document.documentElement.classList.add('dark')
  } else {
    isDarkMode.value = false
    document.documentElement.classList.remove('dark')
  }
})

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}
</script>

<template>
  <div class="relative min-h-screen">
    
    <footer class="fixed bottom-0 right-0 p-4">
      <button
        @click="toggleDarkMode"
        class="bg-[rgb(var(--color-clay-light-input-bg))] dark:bg-[rgb(var(--color-clay-dark-input-bg))] text-[rgb(var(--color-clay-light-text))] dark:text-[rgb(var(--color-clay-dark-text))] px-4 py-2 rounded-full shadow-lg"
      >
        {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
      </button>
    </footer>
    <NuxtPage />
  </div>
</template>