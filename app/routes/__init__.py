from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router
from app.routes.auditoriacomprobante_routes import router as auditoriacomprobante_router
from app.routes.cliente_routes import router as cliente_router
from app.routes.clienteimpuesto_routes import router as clienteimpuesto_router
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


def include_all_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(auditoriacomprobante_router)
    app.include_router(cliente_router)
    app.include_router(clienteimpuesto_router)
    app.include_router(comprobante_router)
    app.include_router(comprobantedetalle_router)
    app.include_router(comprobanteimpuesto_router)
    app.include_router(concepto_router)
    app.include_router(cuentacorriente_router)
    app.include_router(domicilio_router)
    app.include_router(iva_router)
    app.include_router(localidad_router)
    app.include_router(menuitem_router)
    app.include_router(moneda_router)
    app.include_router(operador_router)
    app.include_router(pais_router)
    app.include_router(provincia_router)
    app.include_router(rol_router)
    app.include_router(rolesusuario_router)
    app.include_router(rolmenuitem_router)
    app.include_router(telefono_router)
    app.include_router(tipocomprobante_router)
    app.include_router(tipodoc_router)
    app.include_router(tipodom_router)
    app.include_router(tipoimpuesto_router)
    app.include_router(tipotel_router)
    app.include_router(usuario_router)
    app.include_router(comprobante_full_router)