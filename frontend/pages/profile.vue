<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const user = ref(null)
const router = useRouter()

onMounted(async () => {
  const token = localStorage.getItem('token')
  console.log(token)
  if (token) {
    const response = await fetch('http://localhost:8000/profile', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      user.value = await response.json()
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
  <div class="min-h-screen bg-gray-100 p-8">
    <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md mx-auto">
      <h1 class="text-2xl font-bold mb-6">Profile</h1>
      <div v-if="user">
        <p><strong>Name:</strong> {{ user.name }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
      </div>
      <div v-else>
        <p>Loading...</p>
      </div>
      <button @click="logout" class="mt-6 w-full bg-red-500 text-white py-2 rounded-lg">Logout</button>
    </div>
  </div>
</template>