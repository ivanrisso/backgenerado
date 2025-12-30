import axios from 'axios';
import type { Articulo } from '../../domain/entities/Articulo';
import type { ArticuloRepositoryInterface } from '../../domain/repository/ArticuloRepositoryInterface';

const API_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

export class HttpArticuloRepository implements ArticuloRepositoryInterface {
    async getAll(): Promise<Articulo[]> {
        const response = await axios.get(`${API_URL}/articulos`);
        return response.data;
    }

    async getById(id: number): Promise<Articulo> {
        const response = await axios.get(`${API_URL}/articulos/${id}`);
        return response.data;
    }

    async create(articulo: Articulo): Promise<Articulo> {
        const response = await axios.post(`${API_URL}/articulos/`, articulo);
        return response.data;
    }

    async update(id: number, articulo: Articulo): Promise<Articulo> {
        const response = await axios.patch(`${API_URL}/articulos/${id}`, articulo);
        return response.data;
    }

    async delete(id: number): Promise<void> {
        await axios.delete(`${API_URL}/articulos/${id}`);
    }
}
