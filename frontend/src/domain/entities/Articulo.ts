import type { TipoArticuloEnum } from '../enums/TipoArticuloEnum';
import type { TipoImpuesto } from './TipoImpuesto';

export interface Articulo {
    id: number;
    codigo: string;
    nombre: string;
    descripcion?: string;
    precio_venta: number;
    precio_costo: number;
    tipo: TipoArticuloEnum;
    activo: boolean;

    impuesto_venta_id?: number;
    impuesto_compra_id?: number;

    impuesto_venta?: TipoImpuesto;
    impuesto_compra?: TipoImpuesto;
}
