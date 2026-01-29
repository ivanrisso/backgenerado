import type { TipoDoc } from '../entities/TipoDoc';

export interface ITipoDocRepository {
    getAll: () => Promise<TipoDoc[]>;
    getById: (id: number) => Promise<TipoDoc | null>;
    create: (entity: TipoDoc) => Promise<void>;
    update: (entity: TipoDoc) => Promise<void>;
    delete: (id: number) => Promise<void>;
}
