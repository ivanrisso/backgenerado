
import { TipoAplicacionEnum } from '../enums/TipoAplicacionEnum';
import { BaseTributarioEnum } from '../enums/BaseTributarioEnum';
import { Porcentaje } from '../value-objects/Porcentaje';

export interface TipoImpuesto {
    id: number;
    codigo_afip: string;
    nombre: string;
    descripcion: string;
    tipo_aplicacion: TipoAplicacionEnum;
    base_calculo: BaseTributarioEnum;
    porcentaje?: number; // Could be Porcentaje | null, but interface generally uses primitives or simple objects. If strictly using VO:
    // porcentaje?: Porcentaje; 
    // Keeping it simple as number for the interface, assuming VOs are used in Domain Services or Class Entities.
    // However, user requested "Domain Entities... Value Objects".
    // If I use 'interface', I can't easily force VO usage unless checking types.
    // If I want to enforce rules, I should use Classes or type alias.
    // Let's stick to interface but import Enums. For props like porcentaje, keeping number is standard for DTO/Interface, but for "Pure Domain", VO is better.
    // Let's use the explicit types where possible.
    editable: boolean;
    obligatorio: boolean;
    activo: boolean;
}
