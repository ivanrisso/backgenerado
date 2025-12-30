
import type { Comprobante } from './Comprobante';
import type { ComprobanteDetalle } from './ComprobanteDetalle';
import type { ComprobanteImpuesto } from './ComprobanteImpuesto';

export interface ComprobanteFull extends Comprobante {
    detalles: ComprobanteDetalle[];
    impuestos: ComprobanteImpuesto[];
}
