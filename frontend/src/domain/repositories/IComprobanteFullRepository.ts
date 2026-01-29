
import type { ComprobanteFull } from '../entities/ComprobanteFull';

export interface IComprobanteFullRepository {
    create: (comprobante: ComprobanteFull) => Promise<ComprobanteFull>;
}
