from fastapi import FastAPI, APIRouter
from app.routes.auth_routes import router as auth_router
from app.routes.auditoriacomprobante_routes import router as auditoriacomprobante_router
from app.routes.cliente_routes import router as cliente_router
from app.routes.comprobante_routes import router as comprobante_router
from app.routes.comprobantedetalle_routes import router as comprobantedetalle_router
from app.routes.comprobanteimpuesto_routes import router as comprobanteimpuesto_router
from app.routes.concepto_routes import router as concepto_router
from app.routes.cuentacorriente_routes import router as cuentacorriente_router
from app.routes.domicilio_routes import router as domicilio_router
from app.routes.iva_routes import router as iva_router
from app.routes.localidad_routes import router as localidad_router
from app.routes.menuitem_routes import router as menuitem_router
from app.routes.moneda_routes import router as moneda_router
from app.routes.operador_routes import router as operador_router
from app.routes.pais_routes import router as pais_router
from app.routes.provincia_routes import router as provincia_router
from app.routes.rol_routes import router as rol_router
from app.routes.rolesusuario_routes import router as rolesusuario_router
from app.routes.rolmenuitem_routes import router as rolmenuitem_router
from app.routes.telefono_routes import router as telefono_router
from app.routes.tipocomprobante_routes import router as tipocomprobante_router
from app.routes.tipodoc_routes import router as tipodoc_router
from app.routes.tipodom_routes import router as tipodom_router
from app.routes.tipoimpuesto_routes import router as tipoimpuesto_router
from app.routes.tipotel_routes import router as tipotel_router
from app.routes.usuario_routes import router as usuario_router
from app.routes.comprobante_full_routes import router as comprobante_full_router
from app.routes.condiciontributaria_routes import router as condiciontributaria_router
from app.routes.articulo_routes import router as articulo_router

# Router principal para agrupar todo bajo /api/v1
api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(auditoriacomprobante_router)
api_router.include_router(cliente_router)
api_router.include_router(comprobante_router)
api_router.include_router(comprobantedetalle_router)
api_router.include_router(comprobanteimpuesto_router)
api_router.include_router(concepto_router)
api_router.include_router(cuentacorriente_router)
api_router.include_router(domicilio_router)
api_router.include_router(iva_router)
api_router.include_router(localidad_router)
api_router.include_router(menuitem_router)
api_router.include_router(moneda_router)
api_router.include_router(operador_router)
api_router.include_router(pais_router)
api_router.include_router(provincia_router)
api_router.include_router(rol_router)
api_router.include_router(rolesusuario_router)
api_router.include_router(rolmenuitem_router)
api_router.include_router(telefono_router)
api_router.include_router(tipocomprobante_router)
api_router.include_router(tipodoc_router)
api_router.include_router(tipodom_router)
api_router.include_router(tipoimpuesto_router)
api_router.include_router(tipotel_router)
api_router.include_router(usuario_router)
api_router.include_router(comprobante_full_router)
api_router.include_router(condiciontributaria_router)
api_router.include_router(articulo_router)
from app.routes.recibo_routes import router as recibo_router
api_router.include_router(recibo_router)

from app.routes.afip_config_routes import router as afip_config_router
api_router.include_router(afip_config_router)

from app.routes.punto_venta_routes import router as punto_venta_router
api_router.include_router(punto_venta_router)

def include_all_routes(app: FastAPI):
    app.include_router(api_router)