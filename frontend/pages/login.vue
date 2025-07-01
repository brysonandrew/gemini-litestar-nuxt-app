<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center">
    <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
      <h1 class="text-2xl font-bold mb-6">Login</h1>
      <h2>albo zabka albo terrarium</h2>
      <form @submit.prevent="login">
        <div class="mb-4">
          <label
            for="email"
            class="block text-gray-700"
            >Email</label
          >
          <input
            type="email"
            v-model="email"
            id="email"
            class="w-full px-3 py-2 border rounded-lg"
            required
          />
        </div>
        <div class="mb-6">
          <label
            for="password"
            class="block text-gray-700"
            >Password</label
          >
          <input
            type="password"
            v-model="password"
            id="password"
            class="w-full px-3 py-2 border rounded-lg"
            required
          />
        </div>
        <button
          type="submit"
          class="w-full bg-blue-500 text-white py-2 rounded-lg"
        >
          Login
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const router = useRouter();

async function login() {
  console.log("LOGIN")
  const body = { email: email.value, password: password.value };
  console.log(body);
  const response = await fetch('http://localhost:8000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  console.log(response);

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('token', data.token);
    router.push('/profile');
  } else {
    // Handle login error
    console.error('Login failed');
  }
}
</script>
