
import type { ComprobanteFull } from '../../domain/entities/ComprobanteFull';
import { ComprobanteMapper } from './ComprobanteMapper';
import { Money } from '../../domain/value-objects/Money';

export class ComprobanteFullMapper {
    static toApi(domain: ComprobanteFull): any {
        const header = ComprobanteMapper.toApi(domain);
        return {
            ...header,
            detalles: domain.detalles.map(d => ({
                id: d.id,
                comprobante_id: d.comprobante_id,
                iva_id: d.iva_id,
                descripcion: d.descripcion,
                cantidad: d.cantidad,
                precio_unitario: d.precio_unitario.amount,
                importe: d.importe.amount,
                alicuota_iva: d.alicuota_iva,
                importe_iva: d.importe_iva.amount
            })),
            impuestos: domain.impuestos.map(i => ({
                tipo_impuesto_id: i.tipo_impuesto_id,
                descripcion: i.descripcion,
                base_imponible: i.base_imponible.amount,
                alicuota: i.alicuota,
                importe: i.importe.amount
            }))
        };
    }

    static toDomain(raw: any): ComprobanteFull {
        const header = ComprobanteMapper.toDomain(raw);
        return {
            ...header,
            detalles: (raw.detalles || []).map((d: any) => ({
                id: d.id,
                comprobante_id: d.comprobante_id,
                iva_id: d.iva_id,
                descripcion: d.descripcion,
                cantidad: d.cantidad,
                precio_unitario: new Money(d.precio_unitario),
                importe: new Money(d.importe),
                alicuota_iva: d.alicuota_iva,
                importe_iva: new Money(d.importe_iva)
            })),
            impuestos: (raw.impuestos || []).map((i: any) => ({
                id: i.id,
                comprobante_id: i.comprobante_id,
                tipo_impuesto_id: i.tipo_impuesto_id,
                descripcion: i.descripcion,
                base_imponible: new Money(i.base_imponible),
                alicuota: i.alicuota,
                importe: new Money(i.importe)
            }))
        };
    }
}
