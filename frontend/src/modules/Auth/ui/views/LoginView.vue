<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { loginUseCase } from '@/di';
import { useAuthStore } from '@shared/stores/auth';

const router = useRouter();
const email = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);

const handleLogin = async () => {
    loading.value = true;
    error.value = '';
    try {
        await loginUseCase.execute(email.value, password.value);
        
        // Force hydration of the store before redirecting
        const authStore = useAuthStore();
        await authStore.fetchUser(true);

        // Login successful, redirect to dashboard
        await router.replace('/');
    } catch (e: any) {
        const msg = (e as any).response?.data?.detail;
        error.value = msg || 'Credenciales inválidas o error en el servidor.';
        console.error(e);
    } finally {
        loading.value = false;
    }
};
</script>

<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center p-4">
    <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
      <h1 class="text-2xl font-bold text-gray-900 mb-6 text-center">
        Iniciar Sesión
      </h1>
            
      <form class="space-y-6" @submit.prevent="handleLogin">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
          <input
            id="email" v-model="email" type="email" required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
            placeholder="tu@email.com"
          >
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
          <input
            id="password" v-model="password" type="password" required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
            placeholder="********"
          >
        </div>

        <div v-if="error" class="text-red-600 text-sm text-center">
          {{ error }}
        </div>

        <button
          type="submit" :disabled="loading"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {{ loading ? 'Ingresando...' : 'Ingresar' }}
        </button>
      </form>
    </div>
  </div>
</template>
