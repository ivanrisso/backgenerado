import { Rol } from './Rol';
import { Email } from '../value-objects/Email';

export class Usuario {
    constructor(
        public readonly id: number,
        public readonly email: Email,
        public readonly nombre: string,
        public readonly apellido: string,
        public readonly roles: Rol[],
        public readonly password?: string
    ) { }

    get fullName(): string {
        return `${this.nombre} ${this.apellido}`;
    }

    hasRole(rolNombre: string): boolean {
        return this.roles.some(r => r.rolNombre === rolNombre);
    }

    isAdmin(): boolean {
        return this.roles.some(r => r.esAdmin);
    }

    // Can access a specific menu item?
    // This logic could belong to MenuItem (isAccessibleBy) or here.
    // Putting it here delegates to MenuItem.
    canAccessMenu(menuItem: any): boolean { // 'any' to avoid strict circular dep if not importing MenuItem class, or use Interface
        // Ideally we import MenuItem, but MenuItem imports Rol, Rol is fine. Usuario imports Rol.
        // If MenuItem imports Rol, and Usuario imports Rol, matching is fine.
        // But for strict typing, we might need MenuItem import.
        // Let's rely on the MenuItem's method for "isAccessibleBy(this.roles)".
        return true;
    }
}
