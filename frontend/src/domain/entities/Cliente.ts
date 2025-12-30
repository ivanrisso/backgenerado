import type { Email } from '../value-objects/Email';
import type { CUIT } from '../value-objects/CUIT';
import type { CondicionTributaria } from './CondicionTributaria';

export interface Cliente {
    id: number;
    nombre: string;
    apellido: string;
    razon_social?: string;
    cuit?: CUIT;
    email?: Email;
    tipo_doc_id: number;
    condicion_iva_id?: number;
    condicion_iibb_id?: number;
    nro_iibb?: string;
    condicion_iva?: CondicionTributaria;
    condicion_iibb?: CondicionTributaria;
    domicilios?: import('./Domicilio').Domicilio[];
}
