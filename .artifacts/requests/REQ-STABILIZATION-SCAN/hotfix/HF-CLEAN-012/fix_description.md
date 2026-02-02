# 🔧 Fix Description — HF-CLEAN-012

## Contexto
El maestro tipo de impuestos no funciona correctamente. La primer vez cuando selecciono tipo de impuesto devuelve error.

    at TransformPluginContext._formatLog (file:///home/irisso/proyectos/facturacion/frontend/node_modules/vite/dist/node/chunks/config.js:28998:43)
    at TransformPluginContext.error (file:///home/irisso/proyectos/facturacion/frontend/node_modules/vite/dist/node/chunks/config.js:28995:14)
    at normalizeUrl (file:///home/irisso/proyectos/facturacion/frontend/node_modules/vite/dist/node/chunks/config.js:27118:18)
    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)
    at async file:///home/irisso/proyectos/facturacion/frontend/node_modules/vite/dist/node/chunks/config.js:27176:32
    at async Promise.all (index 11)
    at async TransformPluginContext.transform (file:///home/irisso/proyectos/facturacion/frontend/node_modules/vite/dist/node/chunks/config.js:27144:4)
    at async EnvironmentPluginContainer.transform (file:///home/irisso/proyectos/facturacion/frontend/node_modules/vite/dist/node/chunks/config.js:28796:14)
    at async loadAndTransform (file:///home/irisso/proyectos/facturacion/frontend/node_modules/vite/dist/node/chunks/config.js:22669:26)
    at async viteTransformMiddleware (file:///home/irisso/proyectos/facturacion/frontend/node_modules/vite/dist/node/chunks/config.js:24541:20)
Click outside, press Esc key, or fix the code to dismiss.
You can also disable this overlay by setting server.hmr.overlay to false in vite.config.ts.

## Problema Detectado
Cuando quiero entrar al crud cancela con el error arriba nombrado.

## Causa Raíz


## Alcance de la Corrección
Debe de poder crear, editar, eliminar y leer tipo de impuestos.


## Archivos / Capas Afectadas


## Restricciones
- No romper CI.

## Validaciones Esperadas
- Que cuando hago funcionalmetne el crud se refleje en la pantalla y en la base de datos.

## Notas
Este archivo **NO ejecuta correcciones**.  
Es input directo del Workflow 71.
