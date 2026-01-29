import type { Rol } from './Rol';

export class MenuItem {
    constructor(
        public readonly id: number,
        public readonly nombre: string,
        public readonly path: string | null,
        public readonly parentId: number | null,
        public readonly children: MenuItem[] = [],
        public readonly roles: Rol[] = [] // Public for Vue Proxy compatibility
    ) { }

    get allowedRoles(): Rol[] {
        return [...this.roles];
    }

    addChild(child: MenuItem): void {
        this.children.push(child);
    }

    // Business Logic: Check if a list of roles grants access to this item
    isAccessibleBy(userRoles: Rol[]): boolean {
        if (this.roles.length === 0) return true; // Public if no roles defined? Or default deny? Assuming public if empty for now, or check business rule.
        // Usually empty roles = safe/public or admin only. Let's assume strict ACL: if roles defined, must match.
        // If user is admin (check role property), they might bypass.

        // Check for admin role in userRoles
        if (userRoles.some(r => r.esAdmin)) return true;

        // Check overlap
        return userRoles.some(userRole =>
            this.roles.some(itemRole => itemRole.equals(userRole))
        );
    }
}
