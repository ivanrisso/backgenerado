<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router';
import { logoutUseCase } from '../../di';
import { ref } from 'vue';

const router = useRouter();
const route = useRoute();
// Accordion state. Default to closed unless we are in a sub-route.
const isMaestrosOpen = ref(false);

const handleLogout = async () => {
  try {
    await logoutUseCase.execute();
    router.push('/login');
  } catch (error) {
    console.error('Error logging out:', error);
    router.push('/login'); // Force redirect anyway
  }
};

// Auto-expand if current route is in maestros
if (route.path.includes('/maestros')) {
    isMaestrosOpen.value = true;
}

import { onMounted } from 'vue';
onMounted(() => {
    console.log('MainLayout Mounted');
});
</script>

<template>
  <div class="flex min-h-screen bg-gray-50 font-sans">
    <!-- Sidebar -->
    <aside class="w-64 bg-white border-r border-gray-200 flex flex-col fixed h-full z-10">
      <div class="px-6 py-8 flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-gray-900 flex items-center justify-center text-white font-bold">F</div>
        <span class="text-lg font-semibold tracking-tight text-gray-900">Facturación</span>
      </div>

      <nav class="flex-1 px-4 space-y-1">
        <RouterLink to="/" class="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition-colors" active-class="bg-gray-100 text-gray-900">
          Inicio
        </RouterLink>
        <RouterLink to="/clientes" class="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition-colors" active-class="bg-gray-100 text-gray-900">
          Clientes
        </RouterLink>
        <RouterLink to="/comprobantes" class="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition-colors" active-class="bg-gray-100 text-gray-900">
          Comprobantes
        </RouterLink>

        <!-- Maestros Accordion -->
        <div class="space-y-1">
            <button @click="isMaestrosOpen = !isMaestrosOpen" class="w-full flex items-center justify-between gap-3 px-3 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition-colors">
                <span class="flex items-center gap-3">Maestros</span>
                <span :class="isMaestrosOpen ? 'rotate-90' : ''" class="transition-transform duration-200 text-xs">▶</span>
            </button>
            
            <div v-show="isMaestrosOpen" class="pl-6 space-y-1">
                <RouterLink to="/maestros/tipos-doc" class="block px-3 py-2 text-sm text-gray-500 hover:text-gray-900 rounded-md transition-colors" active-class="text-blue-600 bg-blue-50 font-medium">
                    Tipos Documento
                </RouterLink>
                <RouterLink to="/maestros/tipos-dom" class="block px-3 py-2 text-sm text-gray-500 hover:text-gray-900 rounded-md transition-colors" active-class="text-blue-600 bg-blue-50 font-medium">
                    Tipos Domicilio
                </RouterLink>
                <RouterLink to="/maestros/tipos-tel" class="block px-3 py-2 text-sm text-gray-500 hover:text-gray-900 rounded-md transition-colors" active-class="text-blue-600 bg-blue-50 font-medium">
                    Tipos Teléfono
                </RouterLink>
                <div class="border-t border-gray-100 my-1"></div>
                <RouterLink to="/maestros/paises" class="block px-3 py-2 text-sm text-gray-500 hover:text-gray-900 rounded-md transition-colors" active-class="text-blue-600 bg-blue-50 font-medium">
                    Países
                </RouterLink>
                <RouterLink to="/maestros/provincias" class="block px-3 py-2 text-sm text-gray-500 hover:text-gray-900 rounded-md transition-colors" active-class="text-blue-600 bg-blue-50 font-medium">
                    Provincias
                </RouterLink>
                <RouterLink to="/maestros/localidades" class="block px-3 py-2 text-sm text-gray-500 hover:text-gray-900 rounded-md transition-colors" active-class="text-blue-600 bg-blue-50 font-medium">
                    Localidades
                </RouterLink>
                <div class="border-t border-gray-100 my-1"></div>
                <!-- Auth / Admin -->
                <RouterLink to="/usuarios" class="block px-3 py-2 text-sm text-gray-500 hover:text-gray-900 rounded-md transition-colors" active-class="text-blue-600 bg-blue-50 font-medium">
                    Usuarios
                </RouterLink>
                <RouterLink to="/roles" class="block px-3 py-2 text-sm text-gray-500 hover:text-gray-900 rounded-md transition-colors" active-class="text-blue-600 bg-blue-50 font-medium">
                    Roles
                </RouterLink>
                <RouterLink to="/menu" class="block px-3 py-2 text-sm text-gray-500 hover:text-gray-900 rounded-md transition-colors" active-class="text-blue-600 bg-blue-50 font-medium">
                    Menú
                </RouterLink>
            </div>
        </div>
      </nav>

      <div class="p-4 border-t border-gray-100">
        <div class="flex flex-col gap-3">
          <div class="flex items-center gap-3 px-2">
            <div class="w-8 h-8 rounded-full bg-gray-200"></div>
            <div class="text-sm">
              <div class="font-medium text-gray-900">Admin</div>
              <div class="text-xs text-gray-500">admin@facturacion.com</div>
            </div>
          </div>
          <button @click="handleLogout" class="w-full flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
            Cerrar Sesión
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 ml-64 p-8 max-w-7xl mx-auto w-full">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
</style>
