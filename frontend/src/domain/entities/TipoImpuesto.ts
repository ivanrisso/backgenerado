
import type { TipoAplicacionEnum } from '../enums/TipoAplicacionEnum';
import type { BaseTributarioEnum } from '../enums/BaseTributarioEnum';
import type { AmbitoImpuestoEnum } from '../enums/AmbitoImpuestoEnum';
import type { CategoriaImpuestoEnum } from '../enums/CategoriaImpuestoEnum';
import type { TipoUsoImpuestoEnum } from '../enums/TipoUsoImpuestoEnum';
import type { MetodoCalculoImpuestoEnum } from '../enums/MetodoCalculoImpuestoEnum';
import type { AmbitoUsoImpuestoEnum } from '../enums/AmbitoUsoImpuestoEnum';
import type { CategoriaFiscalImpuestoEnum } from '../enums/CategoriaFiscalImpuestoEnum';
import type { CondicionTributaria } from './CondicionTributaria';
import type { TipoImpuestoDistribucion } from './TipoImpuestoDistribucion';

export interface TipoImpuesto {
    id: number;
    codigo_afip: string;
    nombre: string;
    descripcion: string;
    tipo_aplicacion: TipoAplicacionEnum;
    base_calculo: BaseTributarioEnum;
    ambito: AmbitoImpuestoEnum;
    categoria: CategoriaImpuestoEnum;
    porcentaje?: number;
    editable: boolean;
    obligatorio: boolean;
    activo: boolean;

    // Odoo fields
    tipo_uso: TipoUsoImpuestoEnum;
    metodo_calculo: MetodoCalculoImpuestoEnum;
    ambito_uso: AmbitoUsoImpuestoEnum;
    importe: number;
    etiqueta_factura?: string;
    incluido_precio: boolean;
    afecta_base_subsecuente: boolean;
    categoria_fiscal?: CategoriaFiscalImpuestoEnum;
    notas_legales?: string;
    cuenta_impuesto_vta?: string;
    cuenta_impuesto_com?: string;

    condiciones_asociadas?: CondicionTributaria[];
    reparticiones?: TipoImpuestoDistribucion[];
}

