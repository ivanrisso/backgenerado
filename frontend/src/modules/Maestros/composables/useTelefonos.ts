import { ref } from 'vue';

export function useTelefonos() {
    const telefonos = ref([]);
    const loading = ref(false);
    const error = ref(null);

    const loadTelefonos = async () => { loading.value = true; setTimeout(() => loading.value = false, 500); };
    const createTelefono = async (e: any) => { };
    const updateTelefono = async (e: any) => { };
    const deleteTelefono = async (id: number) => { };

    return { telefonos, loading, error, loadTelefonos, createTelefono, updateTelefono, deleteTelefono };
}
