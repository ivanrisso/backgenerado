import type { Cliente } from '@domain/entities/Cliente';
import { CUIT } from '@domain/value-objects/CUIT';
import { Email } from '@domain/value-objects/Email';

export class ClienteMapper {
    static toDomain(raw: any): Cliente {
        return {
            id: raw.id,
            nombre: raw.nombre,
            apellido: raw.apellido,
            razon_social: raw.razon_social,
            cuit: raw.cuit ? new CUIT(raw.cuit) : undefined,
            email: raw.email ? new Email(raw.email) : undefined,
            tipo_doc_id: raw.tipo_doc_id,
            iva_id: raw.iva_id,
        };
    }

    static toApi(domain: Cliente): any {
        return {
            id: domain.id,
            nombre: domain.nombre,
            apellido: domain.apellido,
            razon_social: domain.razon_social,
            cuit: domain.cuit?.value,
            email: domain.email?.getValue(),
            tipo_doc_id: domain.tipo_doc_id,
            iva_id: domain.iva_id,
        };
    }
}
