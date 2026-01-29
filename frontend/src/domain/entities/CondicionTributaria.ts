import type { AmbitoImpuestoEnum } from '../enums/AmbitoImpuestoEnum';

export interface CondicionTributaria {
    id: number;
    nombre: string;
    descripcion?: string;
    ambito?: AmbitoImpuestoEnum;
    tipo_impuesto_id?: number;
    tipo_impuesto?: any;
}
