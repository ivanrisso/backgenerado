import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'
import { permission } from './shared/directives/permission'
import { setAuthCallbacks } from './shared/http/client'
import { useAuthStore } from './shared/stores/auth'

const pinia = createPinia()

const app = createApp(App)

app.use(pinia)
app.use(router)
app.directive('permission', permission) // Register v-permission

// Handle Auth Callbacks (401 & 403) to avoid circular dependencies
setAuthCallbacks({
    onUnauthorized: (url) => {
        // Prevent infinite loops if related to auth check or login
        if (!url?.includes('/auth/logout') && !url?.includes('/auth/me') && !url?.includes('/auth/login')) {
            const authStore = useAuthStore()
            authStore.logout(false) // Logout locally
        }
    },
    onForbidden: () => {
        router.push({ name: 'forbidden' })
    }
})

app.mount('#app')
