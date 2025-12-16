import { CodigoPais } from '../value-objects/CodigoPais';

export class Pais {
    constructor(
        public readonly id: number,
        public readonly nombre: string,
        public readonly codigo: CodigoPais
    ) {
        if (!nombre) throw new Error("País debe tener un nombre");
    }
}
