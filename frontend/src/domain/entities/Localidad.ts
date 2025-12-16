export class Localidad {
    constructor(
        public readonly id: number,
        public readonly nombre: string,
        public readonly codPostal: string,
        public readonly provinciaId: number
    ) {
        if (!nombre) throw new Error("Localidad debe tener un nombre");
        // codPostal could be a VO if needed, keeping simple for now but strict check could be here
        if (!codPostal) throw new Error("Localidad debe tener código postal");
    }
}
