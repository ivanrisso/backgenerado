
import type { TipoComprobante } from '../entities/TipoComprobante';

export interface ITipoComprobanteRepository {
    getAll: () => Promise<TipoComprobante[]>;
    getById: (id: number) => Promise<TipoComprobante | null>;
    create: (entity: Omit<TipoComprobante, 'id'>) => Promise<TipoComprobante>;
    update: (id: number, entity: Partial<TipoComprobante>) => Promise<TipoComprobante>;
    delete: (id: number) => Promise<void>;
}
