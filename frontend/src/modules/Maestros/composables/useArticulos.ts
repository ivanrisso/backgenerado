import { ref } from 'vue';

export function useArticulos() {
    const articulos = ref([]);
    const loading = ref(false);
    const error = ref(null);

    const loadArticulos = async () => { loading.value = true; setTimeout(() => loading.value = false, 500); };
    const createArticulo = async (e: any) => { };
    const updateArticulo = async (e: any) => { };
    const deleteArticulo = async (id: number) => { };

    return { articulos, loading, error, loadArticulos, createArticulo, updateArticulo, deleteArticulo };
}
