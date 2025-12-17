
export interface Iva {
    id: number;
    codigo: number;
    descripcion: string;
    porcentaje: number; // Keeping number to align with typical JS/JSON serialization patterns for now
    discriminado: boolean;
    porcentaje_sobre: number;
}
