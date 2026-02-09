export interface MenuItem {
    id: string;
    label: string;
    route?: string; // Route name or path
    icon?: string; // Optional: SVG path or icon name
    roles?: string[]; // Roles required to see this item
    permissions?: string[]; // Permissions required
    children?: MenuItem[];
}

export const menuConfig: MenuItem[] = [
    {
        id: 'dashboard',
        label: 'Dashboard',
        route: '/',
        icon: 'home',
        // No roles = public for authenticated users
    },
    {
        id: 'facturacion',
        label: 'Facturación',
        icon: 'document-text',
        children: [
            {
                id: 'comprobantes',
                label: 'Comprobantes',
                route: '/comprobantes',
                permissions: ['comprobante.read']
            },
            // {
            //     id: 'nuevo-comprobante',
            //     label: 'Nueva Factura',
            //     route: '/comprobantes/nuevo',
            //     roles: ['admin', 'vendedor']
            // }
        ]
    },
    {
        id: 'tesoreria',
        label: 'Tesorería',
        icon: 'currency-dollar',
        children: [
            {
                id: 'recibos-list',
                label: 'Recibos',
                route: '/recibos',
                roles: ['admin', 'cobranzas', 'operador']
            },
            {
                id: 'nuevo-recibo',
                label: 'Nuevo Recibo',
                route: '/recibos/nuevo',
                roles: ['admin', 'cobranzas', 'operador']
            }
        ]
    },
    {
        id: 'clientes',
        label: 'Clientes',
        icon: 'users',
        children: [
            {
                id: 'lista-clientes',
                label: 'Directorio',
                route: '/clientes',
                permissions: ['cliente.read'],
                roles: ['admin', 'operador']
            },
            {
                id: 'cuenta-corriente',
                label: 'Cuenta Corriente',
                route: '/cuentacorriente',
                roles: ['admin', 'cobranzas']
            },
            {
                id: 'deudores',
                label: 'Saldos Deudores',
                route: '/clientes/deudores',
                roles: ['admin', 'cobranzas', 'facturacion']
            }
        ]
    },
    {
        id: 'maestros',
        label: 'Maestros',
        icon: 'database',
        roles: ['admin'], // Only admin sees this group
        children: [
            { id: 'monedas', label: 'Monedas', route: '/monedas' },
            { id: 'ivas', label: 'Tasas IVA', route: '/ivas' },
            { id: 'tipos-comprobante', label: 'Tipos Comprobante', route: '/tipos-comprobante' },
            { id: 'tipo-impuestos', label: 'Tipos Impuesto', route: '/tipos-impuesto' },
            { id: 'condiciones-trib', label: 'Cond. Tributarias', route: '/condiciones-tributarias' },
            { id: 'conceptos', label: 'Conceptos', route: '/conceptos' },
            { id: 'tipos-doc', label: 'Tipos Documento', route: '/tipodocs' },
            { id: 'paises', label: 'Países', route: '/paises' },
            { id: 'provincias', label: 'Provincias', route: '/provincias' },
            { id: 'localidades', label: 'Localidades', route: '/localidades' },
            { id: 'tipos-tel', label: 'Tipos Teléfono', route: '/tipotels' },
            // { id: 'domicilios', label: 'Domicilios', route: '/domicilios' },
            { id: 'operadores', label: 'Operadores', route: '/operadores' }
        ]
    },
    {
        id: 'sistema',
        label: 'Sistema',
        icon: 'cog',
        roles: ['admin'],
        children: [
            { id: 'usuarios', label: 'Usuarios', route: '/usuarios' },
            { id: 'roles', label: 'Roles', route: '/roles' },
            { id: 'menus', label: 'Menús', route: '/menus' }
        ]
    }
];
