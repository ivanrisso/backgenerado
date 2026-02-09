export interface ImputacionCreate {
    comprobante_deuda_id: number;
    importe: number;
}

export interface ReciboCreate {
    cliente_id: number;
    fecha_emision: string; // YYYY-MM-DD
    punto_venta: number;
    total: number;
    observaciones?: string;
    imputaciones: ImputacionCreate[];
}

export interface ReciboResponse {
    id: number;
    numero: number;
    fecha_emision: string;
    total: number;
    saldo: number;
    cliente_id: number;
    nombre_cliente?: string;
    observaciones?: string;
}
