import type { Pais } from '../entities/Pais';

export interface IPaisRepository {
    getAll: () => Promise<Pais[]>;
    getById: (id: number) => Promise<Pais | null>;
    create: (entity: Pais) => Promise<void>;
    update: (entity: Pais) => Promise<void>;
    delete: (id: number) => Promise<void>;
}
