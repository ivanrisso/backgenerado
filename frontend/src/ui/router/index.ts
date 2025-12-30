import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@ui/layouts/MainLayout.vue'
import { getProfileUseCase } from '../../di';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/login',
            name: 'login',
            component: () => import('@ui/views/LoginView.vue')
        },
        {
            path: '/',
            component: MainLayout,
            meta: { requiresAuth: true },
            children: [
                {
                    path: '',
                    name: 'home',
                    component: () => import('@ui/views/HomeView.vue')
                },
                {
                    path: 'clientes',
                    name: 'clientes',
                    component: () => import('@ui/views/ClienteList.vue')
                },
                {
                    path: 'clientes/new',
                    name: 'clientes-new',
                    component: () => import('@ui/views/ClienteForm.vue')
                },
                {
                    path: 'clientes/:id/edit',
                    name: 'clientes-edit',
                    component: () => import('@ui/views/ClienteForm.vue')
                },
                {
                    path: 'comprobantes',
                    name: 'comprobantes',
                    component: () => import('@ui/views/HomeView.vue') // Placeholder
                },
                {
                    path: 'configuracion',
                    name: 'configuracion',
                    component: () => import('@ui/views/ConfiguracionView.vue')
                },
                // Auth & RBAC Routes
                {
                    path: 'usuarios',
                    name: 'usuarios',
                    component: () => import('@ui/views/auth/UsuarioList.vue')
                },
                {
                    path: 'roles',
                    name: 'roles',
                    component: () => import('@ui/views/auth/RolList.vue')
                },
                {
                    path: 'menu',
                    name: 'menu',
                    component: () => import('@ui/views/auth/MenuItemTree.vue')
                },
                // Maestros Routes
                {
                    path: 'maestros/tipos-doc',
                    name: 'maestros-tipos-doc',
                    component: () => import('@ui/views/maestros/TipoDocView.vue')
                },
                {
                    path: 'maestros/tipos-dom',
                    name: 'maestros-tipos-dom',
                    component: () => import('@ui/views/maestros/TipoDomView.vue')
                },
                {
                    path: 'maestros/tipos-tel',
                    name: 'maestros-tipos-tel',
                    component: () => import('@ui/views/maestros/TipoTelView.vue')
                },
                {
                    path: 'maestros/paises',
                    name: 'maestros-paises',
                    component: () => import('@ui/views/maestros/PaisView.vue')
                },
                {
                    path: 'maestros/provincias',
                    name: 'maestros-provincias',
                    component: () => import('@ui/views/maestros/ProvinciaView.vue')
                },
                {
                    path: 'maestros/localidades',
                    name: 'maestros-localidades',
                    component: () => import('@ui/views/maestros/LocalidadView.vue')
                },
                {
                    path: 'maestros/tipos-impuesto',
                    name: 'maestros-tipos-impuesto',
                    component: () => import('@ui/views/maestros/TipoImpuestoView.vue')
                },
                {
                    path: 'maestros/articulos',
                    name: 'maestros-articulos',
                    component: () => import('@ui/views/maestros/ArticuloView.vue')
                },
            ]
        }
    ]
})

router.beforeEach(async (to, _from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

    if (requiresAuth) {
        try {
            await getProfileUseCase.execute();
            next();
        } catch (error) {
            next('/login');
        }
    } else {
        // If going to login and already authenticated, redirect home
        if (to.path === '/login') {
            try {
                await getProfileUseCase.execute();
                next('/');
                return;
            } catch (e) {
                // Not authenticated, proceed to login
            }
        }
        next();
    }
});

export default router
