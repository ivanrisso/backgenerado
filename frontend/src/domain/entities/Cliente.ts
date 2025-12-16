import type { Email } from '../value-objects/Email';
import type { CUIT } from '../value-objects/CUIT';

export interface Cliente {
    id: number;
    nombre: string;
    apellido: string;
    razon_social?: string;
    cuit?: CUIT;
    email?: Email;
    tipo_doc_id: number;
    iva_id: number;
}
