
import type { Moneda } from '../entities/Moneda';

export interface IMonedaRepository {
    getAll: () => Promise<Moneda[]>;
    getById: (id: number) => Promise<Moneda | null>;
    create: (entity: Omit<Moneda, 'id'>) => Promise<Moneda>;
    update: (id: number, entity: Partial<Moneda>) => Promise<Moneda>;
    delete: (id: number) => Promise<void>;
}
