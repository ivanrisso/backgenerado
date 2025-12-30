
import type { Telefono } from '../entities/Telefono';

export interface ITelefonoRepository {
    getAll(): Promise<Telefono[]>;
    getByDomicilio(domicilioId: number): Promise<Telefono[]>;
    getById(id: number): Promise<Telefono | null>;
    create(telefono: Omit<Telefono, 'id'>): Promise<Telefono>;
    update(id: number, telefono: Partial<Telefono>): Promise<Telefono>;
    delete(id: number): Promise<void>;
}
