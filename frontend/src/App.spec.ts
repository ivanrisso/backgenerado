
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from './App.vue'

describe('Smoke Test - App.vue', () => {
    it('renders properly', () => {
        // Montaje básico (smoke test)
        const wrapper = mount(App)

        // Verificamos que el componente montado existe
        expect(wrapper.exists()).toBe(true)
    })
})
