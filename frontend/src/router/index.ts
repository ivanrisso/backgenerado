import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@shared/ui/layouts/MainLayout.vue'

import { useAuthStore } from '@shared/stores/auth'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/login',
            name: 'login',
            component: () => import('@modules/Auth/ui/views/LoginView.vue')
        },
        {
            path: '/403',
            name: 'forbidden',
            component: () => import('@shared/ui/views/ForbiddenView.vue')
        },
        {
            path: '/',
            component: MainLayout,
            meta: { requiresAuth: true },
            children: [
                {
                    path: '',
                    name: 'dashboard',
                    component: () => import('@modules/Dashboard/ui/views/DashboardView.vue')
                },
                {
                    path: '/usuarios',
                    name: 'usuarios',
                    component: () => import('@modules/Auth/ui/views/UsuarioList.vue')
                },
                {
                    path: '/clientes',
                    name: 'clientes',
                    component: () => import('@modules/Clientes/ui/views/ClienteList.vue')
                },
                {
                    path: '/clientes/deudores',
                    name: 'clientes-deudores',
                    component: () => import('@modules/Clientes/ui/views/ClienteDeudorList.vue')
                },
                {
                    path: '/clientes/:clienteId/domicilios/:domicilioId/telefonos',
                    name: 'cliente-domicilio-telefonos',
                    component: () => import('@modules/Clientes/ui/views/ClienteTelefonosView.vue')
                },
                {
                    path: '/roles',
                    name: 'roles',
                    component: () => import('@modules/Auth/ui/views/RolList.vue')
                },
                {
                    path: '/menus',
                    name: 'menus',
                    component: () => import('@modules/Auth/ui/views/MenuItemTree.vue')
                },
                // Maestros
                { path: '/monedas', name: 'monedas', component: () => import('@modules/Maestros/ui/views/MonedaView.vue') },
                { path: '/ivas', name: 'ivas', component: () => import('@modules/Maestros/ui/views/IvaView.vue') },
                { path: '/conceptos', name: 'conceptos', component: () => import('@modules/Maestros/ui/views/ConceptoView.vue') },
                { path: '/tipos-comprobante', name: 'tipos-comprobante', component: () => import('@modules/Maestros/ui/views/TipoComprobanteView.vue') },
                { path: '/tipos-impuesto', name: 'tipos-impuesto', component: () => import('@modules/Maestros/ui/views/TipoImpuestoView.vue') },
                { path: '/paises', name: 'paises', component: () => import('@modules/Maestros/ui/views/PaisView.vue') },
                { path: '/provincias', name: 'provincias', component: () => import('@modules/Maestros/ui/views/ProvinciaView.vue') },
                { path: '/localidades', name: 'localidades', component: () => import('@modules/Maestros/ui/views/LocalidadView.vue') },
                { path: '/tipodoms', name: 'tipodoms', component: () => import('@modules/Maestros/ui/views/TipoDomView.vue') },
                { path: '/tipotels', name: 'tipotels', component: () => import('@modules/Maestros/ui/views/TipoTelView.vue') },
                { path: '/operadores', name: 'operadores', component: () => import('@modules/Maestros/ui/views/OperadorView.vue') },
                { path: '/domicilios', name: 'domicilios', component: () => import('@modules/Maestros/ui/views/DomicilioView.vue') },
                { path: '/telefonos', name: 'telefonos', component: () => import('@modules/Maestros/ui/views/TelefonoView.vue') },
                { path: '/tipodocs', name: 'tipodocs', component: () => import('@modules/Maestros/ui/views/TipoDocView.vue') },
                { path: '/condiciones-tributarias', name: 'condiciones-tributarias', component: () => import('@modules/Maestros/ui/views/CondicionTributariaView.vue') },
                { path: '/puntos-venta', name: 'puntos-venta', component: () => import('@modules/Maestros/ui/views/PuntoVentaList.vue') },

                // Config
                { path: '/config/afip', name: 'afip-config', component: () => import('@modules/Maestros/ui/views/AfipConfigView.vue') },

                // Comprobantes
                { path: '/comprobantes/nuevo', name: 'comprobante-nuevo', component: () => import('@modules/Facturacion/ui/views/InvoiceCreateView.vue') },
                { path: '/comprobantes', name: 'comprobantes', component: () => import('@modules/Facturacion/ui/views/InvoiceListView.vue') },

                // Tesorería
                { path: '/recibos', name: 'recibos', component: () => import('@modules/Tesoreria/ui/views/ReciboListView.vue') },
                { path: '/recibos/nuevo', name: 'recibo-nuevo', component: () => import('@modules/Tesoreria/ui/views/ReciboCreateView.vue') },
                { path: '/recibos/:id', name: 'recibo-detalle', component: () => import('@modules/Tesoreria/ui/views/ReciboDetailView.vue') },
                { path: '/recibos/imprimir/:id', name: 'recibo-imprimir', component: () => import('@modules/Tesoreria/ui/views/ReciboPrintView.vue') },
                { path: '/recibos/eliminar/:id', name: 'recibo-eliminar', component: () => import('@modules/Tesoreria/ui/views/ReciboDeleteView.vue') },
                { path: '/recibos/modificar/:id', name: 'recibo-modificar', component: () => import('@modules/Tesoreria/ui/views/ReciboModifyView.vue') },

                // Cliente - Cuenta Corriente
                { path: '/cuentacorriente', name: 'cuentacorriente', component: () => import('@modules/Clientes/ui/views/CurrentAccountView.vue') },
            ]
        }
    ]
})

router.beforeEach(async (to, _from, next) => {
    const authStore = useAuthStore()

    // 1. Attempt hydration if state is idle/failed, or if we have no user but might have cookies.
    // If not authenticated, fetchUser will fail silently and state remains !isAuthenticated
    if (!authStore.isAuthenticated && authStore.hydrationState !== 'loaded') {
        await authStore.fetchUser()
    }

    // 2. Auth Check
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        return next({ name: 'login' })
    }

    // 3. RBAC Check (Roles & Permissions)
    const requiredRoles = to.meta.roles as string[] | undefined
    const requiredPermissions = to.meta.permissions as string[] | undefined

    if (requiredRoles || requiredPermissions) {
        const hasAccess = authStore.canAccess({
            roles: requiredRoles,
            permissions: requiredPermissions
        })

        if (!hasAccess) {
            return next({ name: 'forbidden' })
        }
    }

    next()
})

export default router
