import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../ui/layouts/MainLayout.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/login',
            name: 'login',
            component: () => import('../ui/views/LoginView.vue')
        },
        {
            path: '/',
            component: MainLayout,
            meta: { requiresAuth: true },
            children: [
                {
                    path: '',
                    redirect: '/usuarios'
                },
                {
                    path: '/usuarios',
                    name: 'usuarios',
                    component: () => import('../ui/views/auth/UsuarioList.vue')
                },
                {
                    path: '/clientes',
                    name: 'clientes',
                    component: () => import('../ui/views/clientes/ClienteList.vue')
                },
                {
                    path: '/clientes/:clienteId/domicilios/:domicilioId/telefonos',
                    name: 'cliente-domicilio-telefonos',
                    component: () => import('../ui/views/clientes/ClienteTelefonosView.vue')
                },
                {
                    path: '/roles',
                    name: 'roles',
                    component: () => import('../ui/views/auth/RolList.vue')
                },
                {
                    path: '/menus',
                    name: 'menus',
                    component: () => import('../ui/views/auth/MenuItemTree.vue')
                },
                // Maestros
                { path: '/monedas', name: 'monedas', component: () => import('../ui/views/maestros/MonedaView.vue') },
                { path: '/ivas', name: 'ivas', component: () => import('../ui/views/maestros/IvaView.vue') },
                { path: '/conceptos', name: 'conceptos', component: () => import('../ui/views/maestros/ConceptoView.vue') },
                { path: '/tipos-comprobante', name: 'tipos-comprobante', component: () => import('../ui/views/maestros/TipoComprobanteView.vue') },
                { path: '/tipos-impuesto', name: 'tipos-impuesto', component: () => import('../ui/views/maestros/TipoImpuestoView.vue') },
                { path: '/paises', name: 'paises', component: () => import('../ui/views/maestros/PaisView.vue') },
                { path: '/provincias', name: 'provincias', component: () => import('../ui/views/maestros/ProvinciaView.vue') },
                { path: '/localidades', name: 'localidades', component: () => import('../ui/views/maestros/LocalidadView.vue') },
                { path: '/tipodoms', name: 'tipodoms', component: () => import('../ui/views/maestros/TipoDomView.vue') },
                { path: '/tipotels', name: 'tipotels', component: () => import('../ui/views/maestros/TipoTelView.vue') },
                { path: '/operadores', name: 'operadores', component: () => import('../ui/views/maestros/OperadorView.vue') },
                { path: '/domicilios', name: 'domicilios', component: () => import('../ui/views/maestros/DomicilioView.vue') },
                { path: '/telefonos', name: 'telefonos', component: () => import('../ui/views/maestros/TelefonoView.vue') },
                { path: '/tipodocs', name: 'tipodocs', component: () => import('../ui/views/maestros/TipoDocView.vue') },
                { path: '/condiciones-tributarias', name: 'condiciones-tributarias', component: () => import('../ui/views/maestros/CondicionTributariaView.vue') },

                // Comprobantes
                { path: '/comprobantes/nuevo', name: 'comprobante-nuevo', component: () => import('../ui/views/comprobantes/InvoiceCreateView.vue') },
                { path: '/comprobantes', name: 'comprobantes', component: () => import('../ui/views/comprobantes/InvoiceListView.vue') },

                // Cliente - Cuenta Corriente
                { path: '/cuentacorriente', name: 'cuentacorriente', component: () => import('../ui/views/clientes/CurrentAccountView.vue') },
            ]
        }
    ]
})

router.beforeEach((to, _from, next) => {
    const isAuthenticated = localStorage.getItem('isLoggedIn') === 'true';
    if (to.meta.requiresAuth && !isAuthenticated) {
        next({ name: 'login' });
    } else {
        next();
    }
});

export default router
