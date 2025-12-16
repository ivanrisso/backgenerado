import type { Cliente } from '../entities/Cliente';

export interface IClienteRepository {
    getAll(): Promise<Cliente[]>;
    getById(id: number): Promise<Cliente | null>;
    save(cliente: Cliente): Promise<Cliente>;
    update(cliente: Cliente): Promise<Cliente>;
    delete(id: number): Promise<void>;
}
