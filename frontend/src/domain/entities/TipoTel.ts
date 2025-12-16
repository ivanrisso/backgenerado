export class TipoTel {
    constructor(
        public readonly id: number,
        public readonly nombre: string
    ) {
        if (!nombre) throw new Error("TipoTel debe tener un nombre");
    }
}
