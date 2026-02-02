import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import ReciboCreateView from './ReciboCreateView.vue';
import { createRouter, createWebHistory } from 'vue-router';

// Mock ReciboService and HttpClient
vi.mock('../../../infrastructure/api/ReciboService', () => ({
    ReciboService: {
        create: vi.fn()
    }
}));

vi.mock('../../../shared/http/client', () => ({
    httpClient: {
        get: vi.fn().mockResolvedValue({ data: [] }),
        post: vi.fn()
    }
}));

describe('reciboCreateView', () => {
    it('renders properly', () => {
        const router = createRouter({
            history: createWebHistory(),
            routes: []
        });

        const wrapper = mount(ReciboCreateView, {
            global: {
                plugins: [router]
            }
        });

        expect(wrapper.text()).toContain('Nuevo Recibo de Cobranza');
        expect(wrapper.find('button').text()).toContain('Cancelar');
    });
});
