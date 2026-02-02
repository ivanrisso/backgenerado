# 🔧 Fix Description — HF-CLEAN-020

## Contexto
En la pantalla de alta de comprobantes o alta de factura al grabar devuelve error de afip. Entre ellos {
    "detail": "502: Error al obtener metadata para comprobante - 'Cliente' object has no attribute 'iva_id'"
}

Debe de poder identificarse el error y los sucesivos errores que puedan venir de afip.

Ahora tira este error AxiosClienteRepository.ts:10  GET http://localhost:5173/api/v1/clientes/ 500 (Internal Server Error)
dispatchXhrRequest @ axios.js?v=ca697bc4:1696
xhr @ axios.js?v=ca697bc4:1573
dispatchRequest @ axios.js?v=ca697bc4:2107
Promise.then
_request @ axios.js?v=ca697bc4:2310
request @ axios.js?v=ca697bc4:2219
Axios.<computed> @ axios.js?v=ca697bc4:2346
wrap @ axios.js?v=ca697bc4:8
getAll @ AxiosClienteRepository.ts:10
loadClientes @ useClientes.ts:19
(anónimo) @ InvoiceCreateView.vue:356
(anónimo) @ chunk-DGANQRCK.js?v=ca697bc4:5049
callWithErrorHandling @ chunk-DGANQRCK.js?v=ca697bc4:2342
callWithAsyncErrorHandling @ chunk-DGANQRCK.js?v=ca697bc4:2349
hook.__weh.hook.__weh @ chunk-DGANQRCK.js?v=ca697bc4:5029
flushPostFlushCbs @ chunk-DGANQRCK.js?v=ca697bc4:2527
flushJobs @ chunk-DGANQRCK.js?v=ca697bc4:2569
Promise.then
queueFlush @ chunk-DGANQRCK.js?v=ca697bc4:2464
queuePostFlushCb @ chunk-DGANQRCK.js?v=ca697bc4:2478
queueEffectWithSuspense @ chunk-DGANQRCK.js?v=ca697bc4:9588
baseWatchOptions.scheduler @ chunk-DGANQRCK.js?v=ca697bc4:6345
effect2.scheduler @ chunk-DGANQRCK.js?v=ca697bc4:2088
trigger @ chunk-DGANQRCK.js?v=ca697bc4:533
endBatch @ chunk-DGANQRCK.js?v=ca697bc4:591
notify @ chunk-DGANQRCK.js?v=ca697bc4:853
trigger @ chunk-DGANQRCK.js?v=ca697bc4:827
set value @ chunk-DGANQRCK.js?v=ca697bc4:1734
finalizeNavigation @ vue-router.js?v=ca697bc4:2213
(anónimo) @ vue-router.js?v=ca697bc4:2151
Promise.then
pushWithRedirect @ vue-router.js?v=ca697bc4:2138
push @ vue-router.js?v=ca697bc4:2089
navigateToCreate @ InvoiceListView.vue:57
callWithErrorHandling @ chunk-DGANQRCK.js?v=ca697bc4:2342
callWithAsyncErrorHandling @ chunk-DGANQRCK.js?v=ca697bc4:2349
invoker @ chunk-DGANQRCK.js?v=ca697bc4:11399Entender este error
InvoiceListView.vue:57 [Vue warn]: Unhandled error during execution of mounted hook 
  at <InvoiceCreateView onVnodeUnmounted=fn<onVnodeUnmounted> ref=Ref< Proxy(Object) {__v_skip: true} > > 
  at <RouterView> 
  at <MainLayout onVnodeUnmounted=fn<onVnodeUnmounted> ref=Ref< Proxy(Object) {__v_skip: true} > > 
  at <RouterView> 
  at <App>
warn$1 @ chunk-DGANQRCK.js?v=ca697bc4:2195
logError @ chunk-DGANQRCK.js?v=ca697bc4:2406
handleError @ chunk-DGANQRCK.js?v=ca697bc4:2398
(anónimo) @ chunk-DGANQRCK.js?v=ca697bc4:2352
Promise.catch
callWithAsyncErrorHandling @ chunk-DGANQRCK.js?v=ca697bc4:2351
hook.__weh.hook.__weh @ chunk-DGANQRCK.js?v=ca697bc4:5029
flushPostFlushCbs @ chunk-DGANQRCK.js?v=ca697bc4:2527
flushJobs @ chunk-DGANQRCK.js?v=ca697bc4:2569
Promise.then
queueFlush @ chunk-DGANQRCK.js?v=ca697bc4:2464
queuePostFlushCb @ chunk-DGANQRCK.js?v=ca697bc4:2478
queueEffectWithSuspense @ chunk-DGANQRCK.js?v=ca697bc4:9588
baseWatchOptions.scheduler @ chunk-DGANQRCK.js?v=ca697bc4:6345
effect2.scheduler @ chunk-DGANQRCK.js?v=ca697bc4:2088
trigger @ chunk-DGANQRCK.js?v=ca697bc4:533
endBatch @ chunk-DGANQRCK.js?v=ca697bc4:591
notify @ chunk-DGANQRCK.js?v=ca697bc4:853
trigger @ chunk-DGANQRCK.js?v=ca697bc4:827
set value @ chunk-DGANQRCK.js?v=ca697bc4:1734
finalizeNavigation @ vue-router.js?v=ca697bc4:2213
(anónimo) @ vue-router.js?v=ca697bc4:2151
Promise.then
pushWithRedirect @ vue-router.js?v=ca697bc4:2138
push @ vue-router.js?v=ca697bc4:2089
navigateToCreate @ InvoiceListView.vue:57
callWithErrorHandling @ chunk-DGANQRCK.js?v=ca697bc4:2342
callWithAsyncErrorHandling @ chunk-DGANQRCK.js?v=ca697bc4:2349
invoker @ chunk-DGANQRCK.js?v=ca697bc4:11399Entender esta advertencia
axios.js?v=ca697bc4:1257 Uncaught (in promise) AxiosError {message: 'Request failed with status code 500', name: 'AxiosError', code: 'ERR_BAD_RESPONSE', config: {…}, request: XMLHttpRequest, …}

## Problema Detectado
Devuelve errores de afip al intentar grabar el comprobante.

## Causa Raíz
No debe estar bien configurado el cliente o el comprobante o el certificado de arca.

## Alcance de la Corrección
Debe de poder identificarse el error y los sucesivos errores que puedan venir de afip.

## Archivos / Capas Afectadas


## Restricciones
- No romper CI.

## Validaciones Esperadas
Debe de poder identificarse el error y los sucesivos errores que puedan venir de afip.

## Notas
Este archivo **NO ejecuta correcciones**.  
Es input directo del Workflow 71.
