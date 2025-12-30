import type { Money } from '../value-objects/Money';
import type { CUIT } from '../value-objects/CUIT';

export interface Comprobante {
    id: number;
    cliente_id: number;
    tipo_comprobante_id: number;
    concepto_id: number;
    tipo_doc_id: number;
    moneda_id: number;

    punto_venta: number;
    numero: number;
    fecha_emision: Date; // Keep as Date object in domain

    // Snapshot of client data
    doc_nro: string;
    nombre_cliente: string;
    cuit_cliente: CUIT;
    domicilio_cliente: string;
    localidad_cliente: string;
    cod_postal_cliente: string;
    provincia_cliente: string;

    cotizacion_moneda: number;

    total_neto: Money;
    total_iva: Money;
    total_impuestos: Money;
    total: Money;
    saldo: Money;

    observaciones?: string;
    cae?: string;
    cae_vencimiento?: Date;
}
