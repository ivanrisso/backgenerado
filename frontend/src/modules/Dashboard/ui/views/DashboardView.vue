<template>
    <div class="dashboard-container">
        <header class="dashboard-header">
            <h1>Bienvenido al Sistema de Facturación</h1>
            <p>Seleccione una acción rápida para comenzar</p>
        </header>

        <section class="actions-grid">
            <!-- Acción: Recibos -->
            <div class="action-card" @click="navigateTo('/recibos/nuevo')">
                <div class="icon-wrapper">
                    <span class="material-icons">receipt</span>
                </div>
                <h3>Nuevo Recibo</h3>
                <p>Registrar una cobranza</p>
            </div>

            <!-- Acción: Comprobantes -->
            <div class="action-card" @click="navigateTo('/comprobantes/nuevo')">
                <div class="icon-wrapper">
                    <span class="material-icons">description</span>
                </div>
                <h3>Nueva Factura</h3>
                <p>Emitir comprobante electrónico</p>
            </div>

            <!-- Acción: Clientes -->
            <div class="action-card" @click="navigateTo('/clientes')">
                <div class="icon-wrapper">
                    <span class="material-icons">people</span>
                </div>
                <h3>Directorio</h3>
                <p>Gestionar clientes y cuentas</p>
            </div>
        </section>
    </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateTo = (path: string) => {
    router.push(path)
}
</script>

<style scoped>
.dashboard-container {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.dashboard-header {
    margin-bottom: 3rem;
    text-align: center;
}

.dashboard-header h1 {
    font-size: 2rem;
    color: var(--color-text-primary, #1e293b);
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.dashboard-header p {
    color: var(--color-text-secondary, #64748b);
    font-size: 1.1rem;
}

.actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    padding: 1rem;
}

.action-card {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.action-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    border-color: #cbd5e1;
}

.icon-wrapper {
    width: 64px;
    height: 64px;
    background: #eff6ff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1.5rem auto;
    color: #3b82f6;
}

.icon-wrapper .material-icons {
    font-size: 32px;
}

.action-card h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #334155;
}

.action-card p {
    color: #64748b;
    font-size: 0.95rem;
}
</style>
