<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const user = ref(null)
const router = useRouter()

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (token) {
    const response = await fetch('http://localhost:8000/profile', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      const result = await response.json()
      user.value = result
      console.log(result)
    } else {
      // Handle error, e.g., token expired or invalid
      console.error('Failed to fetch profile')
      localStorage.removeItem('token')
      router.push('/login')
    }
  } else {
    router.push('/login')
  }
})

function logout() {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-[rgb(var(--color-clay-light-bg))] dark:bg-[rgb(var(--color-clay-dark-bg))] transition-colors duration-300">
    <div class="bg-[rgb(var(--color-clay-light-card))] dark:bg-[rgb(var(--color-clay-dark-card))] p-8 rounded-3xl shadow-clay-light dark:shadow-clay-dark w-full max-w-md mx-auto transition-all duration-300">
      <h1 class="text-2xl font-bold mb-6 text-[rgb(var(--color-clay-light-text))] dark:text-[rgb(var(--color-clay-dark-text))] text-center">Profile</h1>
      <div v-if="user" class="text-[rgb(var(--color-clay-light-text))] dark:text-[rgb(var(--color-clay-dark-text))]">
        <p class="mb-2"><strong>Name:</strong> {{ user.name }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
      </div>
      <div v-else class="text-[rgb(var(--color-clay-light-text))] dark:text-[rgb(var(--color-clay-dark-text))]">
        <p>Loading...</p>
      </div>
      <button @click="logout" class="mt-6 w-full bg-red-500 text-white py-3 rounded-xl font-semibold hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 dark:focus:ring-red-600 shadow-clay-button-light dark:shadow-clay-button-dark transition-all duration-300">Logout</button>
    </div>
  </div>
</template>