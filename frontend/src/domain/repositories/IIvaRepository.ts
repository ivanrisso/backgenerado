
import type { Iva } from '../entities/Iva';

export interface IIvaRepository {
    getAll(): Promise<Iva[]>;
    getById(id: number): Promise<Iva | null>;
    create(entity: Omit<Iva, 'id'>): Promise<Iva>;
    update(id: number, entity: Partial<Iva>): Promise<Iva>;
    delete(id: number): Promise<void>;
}
