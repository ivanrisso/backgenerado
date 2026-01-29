import type { Comprobante } from '../entities/Comprobante';

export interface IComprobanteRepository {
    getAll: () => Promise<Comprobante[]>;
    getById: (id: number) => Promise<Comprobante | null>;
    save: (comprobante: Comprobante) => Promise<Comprobante>;
    // Comprobantes usually are not updated/deleted in strict fiscal systems, but adding for completeness if needed (e.g. drafts)
    update: (comprobante: Comprobante) => Promise<Comprobante>;
}
