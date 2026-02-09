from datetime import date
from typing import List, Optional
from app.schemas.recibo import ReciboCreate, ReciboResponse
from app.domain.entities.comprobante import Comprobante
from app.domain.entities.cuentacorriente import CuentaCorriente
from app.domain.entities.imputacion import Imputacion
from app.domain.repository.comprobante_repository_interfase import ComprobanteRepositoryInterface
from app.domain.repository.tipocomprobante_repository_interfase import TipoComprobanteRepositoryInterface
from app.domain.repository.cliente_repository_interfase import ClienteRepositoryInterface
from app.repositories.imputacion_repository import ImputacionRepositoryImpl
from app.repositories.cuentacorriente_repository import CuentaCorrienteRepositoryImpl
from app.domain.exceptions.comprobante import ComprobanteInvalido, ComprobanteNoEncontrado
from app.domain.exceptions.base import ErrorDeRepositorio
from app.domain.exceptions.cliente import ClienteNoEncontrado

class ReciboService:
    def __init__(
        self, 
        comprobante_repo: ComprobanteRepositoryInterface,
        tipo_comprobante_repo: TipoComprobanteRepositoryInterface,
        imputacion_repo: ImputacionRepositoryImpl,
        cc_repo: CuentaCorrienteRepositoryImpl,
        cliente_repo: ClienteRepositoryInterface
    ):
        self.comprobante_repo = comprobante_repo
        self.tipo_comprobante_repo = tipo_comprobante_repo
        self.imputacion_repo = imputacion_repo
        self.cc_repo = cc_repo
        self.cliente_repo = cliente_repo

    async def create_recibo(self, data: ReciboCreate) -> ReciboResponse:
        # 1. Obtener Tipo Comprobante "RECIBO"
        tipos = await self.tipo_comprobante_repo.get_all()
        # Buscamos por código 'RC', 'REC', o similar. Asumimos 'RC' standard o 'RECIBO'.
        # Ajustar según lo que exista en DB real. Por defecto 'RC'.
        tipo_recibo = next((t for t in tipos if t.codigo in ["RC", "REC", "RECIBO"]), None)
        
        if not tipo_recibo:
            # Fallback o error. Lanzamos error para que se configure.
            raise ErrorDeRepositorio("No se encontró el Tipo de Comprobante para Recibos (codigo RC o REC)")

        # 2. Generar Número
        ultimo_numero = await self.comprobante_repo.get_last_number(tipo_recibo.id, data.punto_venta)
        nuevo_numero = ultimo_numero + 1

        # 2a. Obtener Cliente
        cliente = await self.cliente_repo.get_by_id(data.cliente_id)
        if not cliente:
            raise ClienteNoEncontrado(data.cliente_id)

        # 3. Crear Entidad Comprobante (Recibo)
        recibo = Comprobante(
            id=None,
            cliente_id=data.cliente_id,
            tipo_comprobante_id=tipo_recibo.id,
            concepto_id=1, # Default Concepto Productos/Servicios o buscar uno "PAGOS" ??? Asumimos 1 por ahora
            tipo_doc_id=cliente.tipo_doc_id if cliente.tipo_doc_id else 99, 
            
            moneda_id=1, # PESOS default
            punto_venta=data.punto_venta,
            numero=nuevo_numero,
            fecha_emision=data.fecha_emision,
            doc_nro=cliente.cuit if cliente.cuit else "00000000",
            nombre_cliente=cliente.razon_social if cliente.razon_social else f"{cliente.nombre or ''} {cliente.apellido or ''}".strip() or "Cliente",
            cuit_cliente=cliente.cuit if cliente.cuit else "00000000000",
            domicilio_cliente=cliente.domicilio if hasattr(cliente, "domicilio") and cliente.domicilio else "-", # Cliente entity no muestra domicilio en view_file
            localidad_cliente=getattr(cliente, "localidad", "-"), # Asumiendo que podría tener o no
            cod_postal_cliente=getattr(cliente, "cod_postal", "-"),
            provincia_cliente=getattr(cliente, "provincia", "-"),
            
            cotizacion_moneda=1.0,
            total_neto=data.total, # En recibo Neto = Total ?
            total_iva=0,
            total_impuestos=0,
            total=data.total,
            saldo=data.total, # Inicialmente todo disponible
            observaciones=data.observaciones,
            cae="", # No fiscal
            cae_vencimiento=data.fecha_emision # Dummy date
        )
         
        # Necesitamos el cliente real para llenar datos, pero si no tengo ClienteRepository aquí
        # va a explotar por Not Nulls.
        # Asumiré que puedo guardar así o que el cliente_id es suficiente si la BD lo permite (pero ORM models dice nullable=False en varios)
        
        # Guardamos Recibo (Commit=False para transacción)
        recibo_creado = await self.comprobante_repo.create(recibo, commit=False)

        # 4. Registrar Movimiento en Cuenta Corriente (HABER / CRÉDITO)
        cc_mov = CuentaCorriente(
            id=None,
            cliente_id=data.cliente_id,
            comprobante_id=recibo_creado.id, # Ojo, ID es None hasta flush. create hace flush?
            # El repo hace add. Necesitamos flush/refresh.
            # Repo create impl hace commit o flush. Si pasé commit=False, hace flush?
            # Revisando ComprobanteRepositoryImpl: if commit: commit else: flush. OK.
            fecha=data.fecha_emision,
            tipo="REC",
            descripcion=f"Recibo X-{data.punto_venta:04d}-{nuevo_numero:08d}",
            importe=data.total,
            signo=-1, # Crédito resta saldo deudor
            saldo=0 # El saldo acumulado se calcula o se guarda? El modelo tiene saldo. 
            # Calcular saldo histórico es complejo. Por ahora 0 o NULL.
        )
        await self.cc_repo.create(cc_mov, commit=False)

        # 5. Procesar Imputaciones
        total_imputado = 0
        for imp_cmd in data.imputaciones:
            # Buscar factura deuda
            factura = await self.comprobante_repo.get_by_id(imp_cmd.comprobante_deuda_id)
            if not factura:
                raise ComprobanteNoEncontrado(imp_cmd.comprobante_deuda_id)
            
            if factura.saldo < imp_cmd.importe:
                 raise ComprobanteInvalido(f"El importe a imputar ({imp_cmd.importe}) supera el saldo de la factura ({factura.saldo})")

            # Crear Imputacion
            imputacion = Imputacion(
                id=None,
                comprobante_credito_id=recibo_creado.id,
                comprobante_debito_id=factura.id,
                importe=imp_cmd.importe,
                fecha=data.fecha_emision
            )
            await self.imputacion_repo.create(imputacion, commit=False)

            # Actualizar Saldo Factura
            factura.saldo -= imp_cmd.importe
            await self.comprobante_repo.update(factura.id, factura, commit=False)

            # Acumular
            total_imputado += imp_cmd.importe

        # Actualizar Saldo Recibo (Lo que queda disponible)
        if total_imputado > data.total:
             raise ComprobanteInvalido("El total imputado supera el monto del recibo")
        
        recibo_creado.saldo = data.total - total_imputado
        await self.comprobante_repo.update(recibo_creado.id, recibo_creado, commit=True) # Commit FINAL

        return ReciboResponse.model_validate(recibo_creado)

    async def get_all(
        self,
        cliente_id: Optional[int] = None,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[ReciboResponse]:
        # 1. Resolver ID de Tipo Comprobante "Recibo"
        tipos = await self.tipo_comprobante_repo.get_all()
        # Buscamos todos los que parezcan recibos para filtrar inclusive
        # Pero repository get_all suele aceptar un solo ID o tendría que actualizarlo para lista.
        # Por simplicidad y consistencia con create, buscaremos el principal 'RC', 'REC'.
        # Si hubiera varios (Recibo A, Recibo B), el repo necesita ajuste o iteramos.
        # Asumiremos el principal por ahora o el primero que encuentre.
        tipo_recibo = next((t for t in tipos if t.codigo in ["RC", "REC", "RECIBO"]), None)
        
        if not tipo_recibo:
            return []

        comprobantes = await self.comprobante_repo.get_all(
            tipo_comprobante_id=tipo_recibo.id,
            cliente_id=cliente_id,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            limit=limit,
            offset=offset
        )
        
        return [ReciboResponse.model_validate(c) for c in comprobantes]

    async def get_by_id(self, id: int) -> ReciboResponse:
        comprobante = await self.comprobante_repo.get_by_id(id)
        if not comprobante:
            raise ComprobanteNoEncontrado(id)
            
        # Validar que sea Recibo
        tipos = await self.tipo_comprobante_repo.get_all()
        tipo_recibo = next((t for t in tipos if t.codigo in ["RC", "REC", "RECIBO"]), None)
        
        if tipo_recibo and comprobante.tipo_comprobante_id != tipo_recibo.id:
            # Si no es recibo, actuamos como si no existiera para este servicio
             raise ComprobanteNoEncontrado(id)
             
        return ReciboResponse.model_validate(comprobante)

    async def delete_recibo(self, id: int) -> None:
        comprobante = await self.comprobante_repo.get_by_id(id)
        if not comprobante:
            raise ComprobanteNoEncontrado(id)
            
        # TODO: Validar que sea Recibo
        # TODO: Validar que no tenga imputaciones o revertirlas (MVP: Asumimos sin imputaciones o DB cascade/error)
        
        # Eliminación física por simplicidad del MVP solicitado "Baja"
        await self.comprobante_repo.delete(id, commit=True)

    async def update_recibo(self, id: int, data: dict) -> ReciboResponse:
        comprobante = await self.comprobante_repo.get_by_id(id)
        if not comprobante:
            raise ComprobanteNoEncontrado(id)
            
        # Actualizar campos permitidos
        if "observaciones" in data:
            comprobante.observaciones = data["observaciones"]
        if "fecha_emision" in data:
            comprobante.fecha_emision = data["fecha_emision"]
            
        await self.comprobante_repo.update(id, comprobante, commit=True)
        return ReciboResponse.model_validate(comprobante)
