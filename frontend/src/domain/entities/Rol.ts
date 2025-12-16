// Rol is an entity that defines authority.
// It is used by Users (assignments) and MenuItems (permissions).
export class Rol {
    constructor(
        public readonly id: number,
        public readonly rolNombre: string,
        public readonly esAdmin: boolean
    ) { }

    equals(other: Rol): boolean {
        return this.id === other.id;
    }
}
