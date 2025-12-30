
import type { Money } from '../value-objects/Money';

export interface ComprobanteImpuesto {
    id: number;
    comprobante_id: number;
    tipo_impuesto_id: number;
    descripcion: string;
    base_imponible: Money;
    alicuota: number;
    importe: Money;
}
