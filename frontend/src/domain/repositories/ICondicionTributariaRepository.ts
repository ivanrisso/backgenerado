import type { CondicionTributaria } from '../entities/CondicionTributaria';

export interface ICondicionTributariaRepository {
    getAll(): Promise<CondicionTributaria[]>;
    getById(id: number): Promise<CondicionTributaria | null>;
    create(entity: Omit<CondicionTributaria, 'id'>): Promise<CondicionTributaria>;
    update(id: number, entity: Partial<CondicionTributaria>): Promise<CondicionTributaria>;
    delete(id: number): Promise<void>;
}
