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

<template>
  <div class="min-h-screen flex items-center justify-center bg-[rgb(var(--color-clay-light-bg))] dark:bg-[rgb(var(--color-clay-dark-bg))] transition-colors duration-300">
    <div class="bg-[rgb(var(--color-clay-light-card))] dark:bg-[rgb(var(--color-clay-dark-card))] p-8 rounded-3xl shadow-clay-light dark:shadow-clay-dark w-full max-w-md transition-all duration-300">
      <h1 class="text-2xl font-bold mb-6 text-[rgb(var(--color-clay-light-text))] dark:text-[rgb(var(--color-clay-dark-text))] text-center">Login</h1>
      <form @submit.prevent="login">
        <div class="mb-4">
          <label for="email" class="block text-[rgb(var(--color-clay-light-text))] dark:text-[rgb(var(--color-clay-dark-text))] text-sm font-medium mb-2">Email</label>
          <input
            type="email"
            v-model="email"
            id="email"
            class="w-full px-4 py-2 rounded-xl bg-[rgb(var(--color-clay-light-input-bg))] dark:bg-[rgb(var(--color-clay-dark-input-bg))] text-[rgb(var(--color-clay-light-input-text))] dark:text-[rgb(var(--color-clay-dark-input-text))] placeholder-[rgb(var(--color-clay-light-input-placeholder))] dark:placeholder-[rgb(var(--color-clay-dark-input-placeholder))] focus:outline-none focus:ring-2 focus:ring-blue-400 dark:focus:ring-blue-600 shadow-inner-clay-light dark:shadow-inner-clay-dark transition-all duration-300"
            required
          />
        </div>
        <div class="mb-6">
          <label for="password" class="block text-[rgb(var(--color-clay-light-text))] dark:text-[rgb(var(--color-clay-dark-text))] text-sm font-medium mb-2">Password</label>
          <input
            type="password"
            v-model="password"
            id="password"
            class="w-full px-4 py-2 rounded-xl bg-[rgb(var(--color-clay-light-input-bg))] dark:bg-[rgb(var(--color-clay-dark-input-bg))] text-[rgb(var(--color-clay-light-input-text))] dark:text-[rgb(var(--color-clay-dark-input-text))] placeholder-[rgb(var(--color-clay-light-input-placeholder))] dark:placeholder-[rgb(var(--color-clay-dark-input-placeholder))] focus:outline-none focus:ring-2 focus:ring-blue-400 dark:focus:ring-blue-600 shadow-inner-clay-light dark:shadow-inner-clay-dark transition-all duration-300"
            required
          />
        </div>
        <button
          type="submit"
          class="w-full bg-blue-500 text-white py-3 rounded-xl font-semibold hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 dark:focus:ring-blue-600 shadow-clay-button-light dark:shadow-clay-button-dark transition-all duration-300"
        >
          Login
        </button>
      </form>
    </div>
  </div>
</template>