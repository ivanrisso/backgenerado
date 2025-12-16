export class Provincia {
    constructor(
        public readonly id: number,
        public readonly nombre: string,
        public readonly paisId: number
    ) {
        if (!nombre) throw new Error("Provincia debe tener un nombre");
    }
}
