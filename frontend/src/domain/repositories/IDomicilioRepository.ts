
import type { Domicilio } from '../entities/Domicilio';

export interface IDomicilioRepository {
    getAll: () => Promise<Domicilio[]>;
    getById: (id: number) => Promise<Domicilio | null>;
    create: (domicilio: Omit<Domicilio, 'id'>) => Promise<Domicilio>;
    update: (id: number, domicilio: Partial<Domicilio>) => Promise<Domicilio>;
    delete: (id: number) => Promise<void>;
}
