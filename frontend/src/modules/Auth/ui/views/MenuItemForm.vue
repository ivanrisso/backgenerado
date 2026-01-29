<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue';
import { MenuItem } from '../../../domain/entities/MenuItem';
import { useRoles } from '../../composables/auth/useRoles';

const props = defineProps<{
    modelValue: MenuItem | null;
    parentId?: number | null;
    availableParents?: MenuItem[];
}>();

const emit = defineEmits<{
    (e: 'submit', entity: MenuItem, roleIds: number[]): void;
    (e: 'cancel'): void;
}>();

const { roles: allRoles, loadRoles } = useRoles();

const form = ref({
    id: 0,
    nombre: '',
    path: '',
    parentId: null as number | null,
    roleIds: [] as number[]
});

onMounted(() => {
    loadRoles();
});

// Filter out self from available parents to prevent circular dependency
const validParents = computed(() => {
    return props.availableParents?.filter(p => p.id !== form.value.id) || [];
});

watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = {
            id: newVal.id,
            nombre: newVal.nombre,
            path: newVal.path || '',
            parentId: newVal.parentId,
            roleIds: newVal.roles.map(r => r.id)
        };
    } else {
        form.value = { 
            id: 0, 
            nombre: '', 
            path: '', 
            parentId: props.parentId || null, 
            roleIds: [] 
        };
    }
}, { immediate: true });

const handleSubmit = () => {
    try {
        const selectedRoles = allRoles.value.filter(r => form.value.roleIds.includes(r.id));
        const entity = new MenuItem(
            form.value.id,
            form.value.nombre,
            form.value.path || null,
            form.value.parentId,
            [], // Children handled by tree, not form
            selectedRoles
        );
        emit('submit', entity, form.value.roleIds);
    } catch (e: any) {
        alert(e.message);
    }
};
</script>

<template>
  <div class="bg-gray-50 p-6 rounded-lg border border-gray-200 mb-6 shadow-sm">
    <h3 class="text-lg font-medium text-gray-900 mb-4">
      {{ modelValue ? 'Editar' : 'Nuevo' }} Item de Menú
    </h3>
    <form class="space-y-4" @submit.prevent="handleSubmit">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Nombre</label>
          <input v-model="form.nombre" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Path (Ruta)</label>
          <input v-model="form.path" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" placeholder="/ejemplo">
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Parent (Padre)</label>
        <select v-model="form.parentId" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
          <option :value="null">
            -- Raíz (Sin Padre) --
          </option>
          <option v-for="p in validParents" :key="p.id" :value="p.id">
            {{ p.nombre }}
          </option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Roles con Acceso (Vacío = Todos)</label>
        <div class="flex flex-wrap gap-4 bg-white p-3 rounded border border-gray-200">
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
