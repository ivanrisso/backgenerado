import type { Comprobante } from '@domain/entities/Comprobante';
import { Money } from '@domain/value-objects/Money';
import { CUIT } from '@domain/value-objects/CUIT';

export class ComprobanteMapper {
    static toDomain(raw: any): Comprobante {
        return {
            id: raw.id,
            cliente_id: raw.cliente_id,
            tipo_comprobante_id: raw.tipo_comprobante_id,
            concepto_id: raw.concepto_id,
            tipo_doc_id: raw.tipo_doc_id,
            moneda_id: raw.moneda_id,
            punto_venta: raw.punto_venta,
            numero: raw.numero,
            fecha_emision: new Date(raw.fecha_emision),
            doc_nro: raw.doc_nro,
            nombre_cliente: raw.nombre_cliente,
            cuit_cliente: new CUIT(raw.cuit_cliente),
            domicilio_cliente: raw.domicilio_cliente,
            localidad_cliente: raw.localidad_cliente,
            cod_postal_cliente: raw.cod_postal_cliente,
            provincia_cliente: raw.provincia_cliente,
            cotizacion_moneda: raw.cotizacion_moneda,
            total_neto: new Money(raw.total_neto),
            total_iva: new Money(raw.total_iva),
            total_impuestos: new Money(raw.total_impuestos),
            total: new Money(raw.total),
            saldo: new Money(raw.saldo ?? raw.total), // Default to total if undefined
            observaciones: raw.observaciones,
            cae: raw.cae,
            cae_vencimiento: raw.cae_vencimiento ? new Date(raw.cae_vencimiento) : undefined,
        };
    }

    static toApi(domain: Comprobante): any {
        return {
            ...domain,
            cuit_cliente: domain.cuit_cliente.value,
            fecha_emision: domain.fecha_emision.toISOString().split('T')[0], // YYYY-MM-DD
            total_neto: domain.total_neto.amount,
            total_iva: domain.total_iva.amount,
            total_impuestos: domain.total_impuestos.amount,
            total: domain.total.amount,
        };
    }
}
