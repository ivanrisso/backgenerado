
const fs = require('fs');
const path = require('path');

// Base paths
const PROJECT_ROOT = '/home/irisso/proyectos/facturacion';
const FRONTEND_SRC = path.join(PROJECT_ROOT, 'frontend/src');

// Mappings
const ALIASES = {
    '@shared': path.join(FRONTEND_SRC, 'shared'),
    '@modules': path.join(FRONTEND_SRC, 'modules')
};

// Extracted from router/index.ts
const ROUTES = [
    { path: '/login', component: '@modules/Auth/ui/views/LoginView.vue' },
    { path: '/403', component: '@shared/ui/views/ForbiddenView.vue' },
    // Main Layout skipped (static import)
    { path: '/', component: '@modules/Dashboard/ui/views/DashboardView.vue' },
    { path: '/usuarios', component: '@modules/Auth/ui/views/UsuarioList.vue' },
    { path: '/clientes', component: '@modules/Clientes/ui/views/ClienteList.vue' },
    { path: '/clientes/deudores', component: '@modules/Clientes/ui/views/ClienteDeudorList.vue' },
    { path: '/clientes/:clienteId/domicilios/:domicilioId/telefonos', component: '@modules/Clientes/ui/views/ClienteTelefonosView.vue' },
    { path: '/roles', component: '@modules/Auth/ui/views/RolList.vue' },
    { path: '/menus', component: '@modules/Auth/ui/views/MenuItemTree.vue' },
    { path: '/monedas', component: '@modules/Maestros/ui/views/MonedaView.vue' },
    { path: '/ivas', component: '@modules/Maestros/ui/views/IvaView.vue' },
    { path: '/conceptos', component: '@modules/Maestros/ui/views/ConceptoView.vue' },
    { path: '/tipos-comprobante', component: '@modules/Maestros/ui/views/TipoComprobanteView.vue' },
    { path: '/tipos-impuesto', component: '@modules/Maestros/ui/views/TipoImpuestoView.vue' },
    { path: '/paises', component: '@modules/Maestros/ui/views/PaisView.vue' },
    { path: '/provincias', component: '@modules/Maestros/ui/views/ProvinciaView.vue' },
    { path: '/localidades', component: '@modules/Maestros/ui/views/LocalidadView.vue' },
    { path: '/tipodoms', component: '@modules/Maestros/ui/views/TipoDomView.vue' },
    { path: '/tipotels', component: '@modules/Maestros/ui/views/TipoTelView.vue' },
    { path: '/operadores', component: '@modules/Maestros/ui/views/OperadorView.vue' },
    { path: '/domicilios', component: '@modules/Maestros/ui/views/DomicilioView.vue' },
    { path: '/telefonos', component: '@modules/Maestros/ui/views/TelefonoView.vue' },
    { path: '/tipodocs', component: '@modules/Maestros/ui/views/TipoDocView.vue' },
    { path: '/condiciones-tributarias', component: '@modules/Maestros/ui/views/CondicionTributariaView.vue' },
    { path: '/puntos-venta', component: '@modules/Maestros/ui/views/PuntoVentaList.vue' },
    { path: '/config/afip', component: '@modules/Maestros/ui/views/AfipConfigView.vue' },
    { path: '/comprobantes/nuevo', component: '@modules/Facturacion/ui/views/InvoiceCreateView.vue' },
    { path: '/comprobantes', component: '@modules/Facturacion/ui/views/InvoiceListView.vue' },
    { path: '/recibos', component: '@modules/Tesoreria/ui/views/ReciboListView.vue' },
    { path: '/recibos/nuevo', component: '@modules/Tesoreria/ui/views/ReciboCreateView.vue' },
    { path: '/recibos/:id', component: '@modules/Tesoreria/ui/views/ReciboDetailView.vue' },
    { path: '/recibos/imprimir/:id', component: '@modules/Tesoreria/ui/views/ReciboPrintView.vue' },
    { path: '/recibos/eliminar/:id', component: '@modules/Tesoreria/ui/views/ReciboDeleteView.vue' },
    { path: '/recibos/modificar/:id', component: '@modules/Tesoreria/ui/views/ReciboModifyView.vue' },
    { path: '/cuentacorriente', component: '@modules/Clientes/ui/views/CurrentAccountView.vue' },
];

function checkRoutes() {
    console.log('Checking routes...');
    const report = [];

    ROUTES.forEach(route => {
        let resolvedPath = route.component;
        for (const [alias, realPath] of Object.entries(ALIASES)) {
            if (resolvedPath.startsWith(alias)) {
                resolvedPath = resolvedPath.replace(alias, realPath);
                break;
            }
        }

        const exists = fs.existsSync(resolvedPath);
        report.push({
            path: route.path,
            component: route.component,
            resolvedPath: resolvedPath,
            exists: exists
        });

        if (!exists) {
            console.error(`[MISSING] ${route.path} -> ${route.component}`);
        } else {
            // console.log(`[OK] ${route.path}`);
        }
    });

    console.log(`Checked ${ROUTES.length} routes.`);
    fs.writeFileSync('/home/irisso/proyectos/facturacion/.artifacts/requests/REQ-FUNC-003/architecture/routes_check.json', JSON.stringify(report, null, 2));
}

checkRoutes();
