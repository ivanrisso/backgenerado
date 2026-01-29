<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import { Usuario } from '../../../domain/entities/Usuario';
import { Email } from '../../../domain/value-objects/Email';
import { useRoles } from '../../composables/auth/useRoles';

const props = defineProps<{
    modelValue: Usuario | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: Usuario): void;
    (e: 'cancel'): void;
}>();

const { roles: allRoles, loadRoles } = useRoles();

const form = ref({
    id: 0,
    nombre: '',
    apellido: '',
    email: '',
    password: '',
    roleIds: [] as number[]
});

onMounted(() => {
    loadRoles();
});

watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = {
            id: newVal.id,
            nombre: newVal.nombre,
            apellido: newVal.apellido,
            email: newVal.email instanceof Email ? newVal.email.getValue() : (newVal.email as any),
            password: '', // Password not populated on edit for security
            roleIds: newVal.roles.map(r => r.id)
        };
    } else {
        form.value = { id: 0, nombre: '', apellido: '', email: '', password: '', roleIds: [] };
    }
}, { immediate: true });

const handleSubmit = () => {
    try {
        // Find selected role objects
        const selectedRoles = allRoles.value.filter(r => form.value.roleIds.includes(r.id));
        
        const entity = new Usuario(
            form.value.id,
            new Email(form.value.email),
            form.value.nombre,
            form.value.apellido,
            selectedRoles,
            form.value.password || undefined
        );
        emit('submit', entity);
    } catch (e: any) {
        alert(e.message);
    }
};
</script>

<template>
  <div class="bg-gray-50 p-6 rounded-lg border border-gray-200 mb-6 shadow-sm">
    <h3 class="text-lg font-medium text-gray-900 mb-4">
      {{ modelValue ? 'Editar' : 'Nuevo' }} Usuario
    </h3>
    <form class="space-y-4" @submit.prevent="handleSubmit">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Nombre</label>
          <input v-model="form.nombre" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Apellido</label>
          <input v-model="form.apellido" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
        </div>
      </div>
        
      <div>
        <label class="block text-sm font-medium text-gray-700">Email</label>
        <input v-model="form.email" type="email" autocomplete="off" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
      </div>

      <div v-if="!modelValue">
        <label class="block text-sm font-medium text-gray-700">Contraseña</label>
        <input v-model="form.password" type="password" autocomplete="new-password" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" placeholder="Min. 6 caracteres">
      </div>
      <div v-else>
        <label class="block text-sm font-medium text-gray-700">Nueva Contraseña (Opcional)</label>
        <input v-model="form.password" type="password" autocomplete="new-password" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" placeholder="Dejar en blanco para mantener la actual">
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Roles</label>
        <div class="flex flex-wrap gap-4">
          <div v-for="role in allRoles" :key="role.id" class="flex items-center">
            <input v-model="form.roleIds" type="checkbox" :value="role.id" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded">
            <label class="ml-2 block text-sm text-gray-900">
              {{ role.rolNombre }}
            </label>
          </div>
        </div>
      </div>

      <div class="flex justify-end gap-3 pt-2">
        <button type="button" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500" @click="$emit('cancel')">
          Cancelar
        </button>
        <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
          Guardar
        </button>
      </div>
    </form>
  </div>
</template>
