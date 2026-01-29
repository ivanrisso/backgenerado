import type { Directive } from 'vue';
import { useAuthStore } from '../stores/auth';

export const permission: Directive = {
    mounted(el, binding) {
        const { value } = binding;
        const authStore = useAuthStore();

        if (!value) {
            throw new Error('v-permission needs a value! Like v-permission="[\'admin\', \'editor\']"');
        }

        // Supports literal string, array of strings, or object configuration
        // Passed directly to authStore.canAccess which handles normalization
        const hasAccess = authStore.canAccess(value);

        if (!hasAccess) {
            el.parentNode && el.parentNode.removeChild(el);
        }
    }
};
