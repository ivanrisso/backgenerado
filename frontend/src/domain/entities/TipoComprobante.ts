
// import { CodigoArca } from '../value-objects/CodigoArca'; 
// Using basic types for Interface as discussed, but documenting intention.
// Ideally, strict DDD uses VOs in interfaces.
// Let's TRY to use the VO in the interface for better semantics.

import { CodigoArca } from '../value-objects/CodigoArca';

export interface TipoComprobante {
    id: number;
    codigo: string;
    descripcion: string;
    es_fiscal: boolean;
    codigo_arca: string; // Keeping string for simplicity in frontend binding, usually VOs are unwrapped for UI or DTOs. 
    // But for "Domain Layer", it should be CodigoArca.
    // However, typical Vue bindings work better with primitives.
    // I will keep string in the interface but the domain logic (if any) should use VOs.
    // Given the "light DDD" constraint, I'll stick to primitives in Interfaces but provide VOs for validation logic.
}
