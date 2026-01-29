import type { Provincia } from '../entities/Provincia';

export interface IProvinciaRepository {
    getAll: () => Promise<Provincia[]>;
    getById: (id: number) => Promise<Provincia | null>;
    getAllByPais: (paisId: number) => Promise<Provincia[]>;
    create: (entity: Provincia) => Promise<void>;
    update: (entity: Provincia) => Promise<void>;
    delete: (id: number) => Promise<void>;
}
