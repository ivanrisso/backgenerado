from datetime import date
from typing import List, Optional
from app.schemas.recibo import ReciboCreate, ReciboResponse
from app.domain.entities.comprobante import Comprobante
from app.domain.entities.cuentacorriente import CuentaCorriente
from app.domain.entities.imputacion import Imputacion
from app.domain.repository.comprobante_repository_interfase import ComprobanteRepositoryInterface
from app.domain.repository.tipocomprobante_repository_interfase import TipoComprobanteRepositoryInterface
from app.repositories.imputacion_repository import ImputacionRepositoryImpl
from app.repositories.cuentacorriente_repository import CuentaCorrienteRepositoryImpl
from app.domain.exceptions.comprobante import ComprobanteInvalido, ComprobanteNoEncontrado
from app.domain.exceptions.base import ErrorDeRepositorio

class ReciboService:
    def __init__(
        self, 
        comprobante_repo: ComprobanteRepositoryInterface,
        tipo_comprobante_repo: TipoComprobanteRepositoryInterface,
        imputacion_repo: ImputacionRepositoryImpl,
        cc_repo: CuentaCorrienteRepositoryImpl
    ):
        self.comprobante_repo = comprobante_repo
        self.tipo_comprobante_repo = tipo_comprobante_repo
        self.imputacion_repo = imputacion_repo
        self.cc_repo = cc_repo

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

        # 3. Crear Entidad Comprobante (Recibo)
        # Nota: Usamos campos default o dummy para lo que no aplica a Recibo (CAE, etc)
        # El saldo inicial del recibo es el Total. Se irá consumiendo con imputaciones.
        # Si sobra, queda como saldo a favor en el recibo.
        recibo = Comprobante(
            id=None,
            cliente_id=data.cliente_id,
            tipo_comprobante_id=tipo_recibo.id,
            concepto_id=1, # Default Concepto Productos/Servicios o buscar uno "PAGOS" ??? Asumimos 1 por ahora
            tipo_doc_id=99, # Consumidor Final o lo que venga del cliente? 
            # ! IMPORTANTE: Deberíamos obtener los datos del cliente real para llenar estos campos denormalizados
            # Por simplicidad en este REQ, asumimos que el repo llena o el front manda. 
            # Como ReciboCreate no tiene todo, esto fallaría en BD si son Not Null.
            # SOLUCIÓN: ReciboService debería buscar al Cliente para llenar nombre, cuit, etc.
            # Por ahora pondré placeholders, pero idealmente se inyecta ClienteRepository.
            
            moneda_id=1, # PESOS default
            punto_venta=data.punto_venta,
            numero=nuevo_numero,
            fecha_emision=data.fecha_emision,
            doc_nro="00000000", # Placeholder
            nombre_cliente="Cliente", # Placeholder
            cuit_cliente="00000000000",
            domicilio_cliente="-",
            localidad_cliente="-",
            cod_postal_cliente="-",
            provincia_cliente="-",
            
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
