
import type { Concepto } from '../entities/Concepto';

export interface IConceptoRepository {
    getAll: () => Promise<Concepto[]>;
    getById: (id: number) => Promise<Concepto | null>;
    create: (entity: Omit<Concepto, 'id'>) => Promise<Concepto>;
    update: (id: number, entity: Partial<Concepto>) => Promise<Concepto>;
    delete: (id: number) => Promise<void>;
}
