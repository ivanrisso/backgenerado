
import type { Operador } from '../entities/Operador';

export interface IOperadorRepository {
    getAll(): Promise<Operador[]>;
    getById(id: number): Promise<Operador | null>;
    create(entity: Omit<Operador, 'id'>): Promise<Operador>;
    update(id: number, entity: Partial<Operador>): Promise<Operador>;
    delete(id: number): Promise<void>;
}
