import { httpClient } from '@/shared/http/client';

export interface PuntoVenta {
    id: number;
    numero: number;
    tipo: 'ELECTRONICA' | 'FISCAL' | 'MANUAL';
    bloqueado: boolean;
}

export type PuntoVentaCreate = Omit<PuntoVenta, 'id'>;
export type PuntoVentaUpdate = Partial<PuntoVentaCreate>;

const BASE_URL = '/puntos-venta';

export const puntoVentaApi = {
    getAll: async (): Promise<PuntoVenta[]> => {
        const response = await httpClient.get<PuntoVenta[]>(BASE_URL);
        return response.data;
    },

    getById: async (id: number): Promise<PuntoVenta> => {
        const response = await httpClient.get<PuntoVenta>(`${BASE_URL}/${id}`);
        return response.data;
    },

    create: async (data: PuntoVentaCreate): Promise<PuntoVenta> => {
        const response = await httpClient.post<PuntoVenta>(BASE_URL, data);
        return response.data;
    },

    update: async (id: number, data: PuntoVentaUpdate): Promise<PuntoVenta> => {
        const response = await httpClient.put<PuntoVenta>(`${BASE_URL}/${id}`, data);
        return response.data;
    },

    delete: async (id: number): Promise<void> => {
        await httpClient.delete(`${BASE_URL}/${id}`);
    }
};
