import type { Money } from '../value-objects/Money';

export interface ComprobanteDetalle {
    id: number;
    comprobante_id: number;
    iva_id: number;
    descripcion: string;
    cantidad: number;
    precio_unitario: Money;
    importe: Money;
    alicuota_iva: number;
    importe_iva: Money;
}
