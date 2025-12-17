
import type { TipoImpuesto } from '../entities/TipoImpuesto';

export interface ITipoImpuestoRepository {
    getAll(): Promise<TipoImpuesto[]>;
    getById(id: number): Promise<TipoImpuesto | null>;
    create(entity: Omit<TipoImpuesto, 'id'>): Promise<TipoImpuesto>;
    update(id: number, entity: Partial<TipoImpuesto>): Promise<TipoImpuesto>;
    delete(id: number): Promise<void>;
}
