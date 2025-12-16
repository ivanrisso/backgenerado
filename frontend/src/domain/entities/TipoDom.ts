export class TipoDom {
    constructor(
        public readonly id: number,
        public readonly nombre: string
    ) {
        if (!nombre) throw new Error("TipoDom debe tener un nombre");
    }
}
