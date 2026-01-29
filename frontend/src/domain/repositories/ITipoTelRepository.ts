import type { TipoTel } from '../entities/TipoTel';

export interface ITipoTelRepository {
    getAll: () => Promise<TipoTel[]>;
    getById: (id: number) => Promise<TipoTel | null>;
    create: (entity: TipoTel) => Promise<void>;
    update: (entity: TipoTel) => Promise<void>;
    delete: (id: number) => Promise<void>;
}
