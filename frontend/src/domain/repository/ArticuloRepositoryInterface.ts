import type { Articulo } from '../entities/Articulo';

export interface ArticuloRepositoryInterface {
    getAll: () => Promise<Articulo[]>;
    getById: (id: number) => Promise<Articulo>;
    create: (articulo: Articulo) => Promise<Articulo>;
    update: (id: number, articulo: Articulo) => Promise<Articulo>;
    delete: (id: number) => Promise<void>;
}
