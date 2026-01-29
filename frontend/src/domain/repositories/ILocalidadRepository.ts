import type { Localidad } from '../entities/Localidad';

export interface ILocalidadRepository {
    getAll: () => Promise<Localidad[]>;
    getById: (id: number) => Promise<Localidad | null>;
    getAllByProvincia: (provinciaId: number) => Promise<Localidad[]>;
    create: (entity: Localidad) => Promise<void>;
    update: (entity: Localidad) => Promise<void>;
    delete: (id: number) => Promise<void>;
}
