import { CodigoArca } from '../value-objects/CodigoArca';

export class TipoDoc {
    constructor(
        public readonly id: number,
        public readonly nombre: string,
        public readonly habilitado: boolean,
        public readonly codigoArca: CodigoArca
    ) {
        if (!nombre) throw new Error("TipoDoc debe tener un nombre");
    }

    // Example logic: Check if it's usable
    esValidoParaFacturar(): boolean {
        return this.habilitado;
    }
}
