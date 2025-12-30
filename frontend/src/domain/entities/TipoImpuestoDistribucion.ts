export enum TipoDistribucionImpuestoEnum {
    FACTURA = 'factura',
    REEMBOLSO = 'reembolso'
}

export enum TipoReparticionBaseImpuestoEnum {
    BASE = 'base',
    IMPUESTO = 'impuesto'
}

export interface TipoImpuestoEtiqueta {
    id: number;
    nombre: string;
    descripcion?: string;
}

export interface TipoImpuestoDistribucion {
    id?: number;
    tipo_impuesto_id?: number;
    tipo_reparticion: TipoDistribucionImpuestoEnum;
    factor_porcentaje: number;
    basado_en: TipoReparticionBaseImpuestoEnum;
    etiqueta_id?: number;
    cuenta_contable?: string;
    etiqueta?: TipoImpuestoEtiqueta;
}
