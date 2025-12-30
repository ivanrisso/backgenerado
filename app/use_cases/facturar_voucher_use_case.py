from app.domain.repository.voucher_repository_interface import VoucherRepositoryInterface
from app.use_cases.comprobante_full_use_case import ComprobanteFullUseCase
from app.schemas.comprobante_full import ComprobanteFullCreate, ComprobanteDetalleCreate
from app.schemas.comprobante_impuesto import ComprobanteImpuestoCreate
from app.domain.entities.voucher import Voucher
from app.domain.repository.cliente_repository_interfase import ClienteRepositoryInterface
from app.domain.repository.tipoimpuesto_repository_interfase import TipoImpuestoRepositoryInterface
from app.domain.repository.iva_repository_interfase import IvaRepositoryInterface
from app.domain.exceptions.comprobante import ComprobanteDuplicado, ComprobanteInvalido, ComprobanteNoEncontrado
import logging

logger = logging.getLogger(__name__)

class FacturarVoucherUseCase:
    def __init__(self, 
                 voucher_repo: VoucherRepositoryInterface,
                 comprobante_use_case: ComprobanteFullUseCase,
                 cliente_repo: ClienteRepositoryInterface,
                 iva_repo: IvaRepositoryInterface,
                 tipo_impuesto_repo: TipoImpuestoRepositoryInterface):
        self.voucher_repo = voucher_repo
        self.comprobante_use_case = comprobante_use_case
        self.cliente_repo = cliente_repo
        self.iva_repo = iva_repo
        self.tipo_impuesto_repo = tipo_impuesto_repo

    async def execute(self, voucher_id: str, cliente_id: int, punto_venta: int, tipo_comprobante_id: int, concepto_id: int):
        # 1. Fetch Client Data
        client = await self.cliente_repo.get_by_id(cliente_id)
        if not client:
            raise ComprobanteInvalido(f"Cliente {cliente_id} no encontrado.")

        # 2. Determine Taxes from Cliente direct fields
        iva_rate = 21.0 # Default fallback
        client_iva_id = 1 # Default fallback (assuming 1 is 21%)
        other_taxes = []

        # Helper to find IVA ID by rate from DB
        all_ivas = await self.iva_repo.get_all()
        
        if client.condicion_iva_id:
            cond = client.condicion_iva
            # Check if this condition implies a specific IVA rate?
            # For now, we'll try to guess or use the first standard IVA found.
            # In a real scenario, CondicionTributaria might link to a default Iva entity.
            # Here we follow the legacy logic but adapted:
            if cond and "RESPONSABLE INSCRIPTO" in (cond.nombre or "").upper():
                iva_rate = 21.0
                for i_obj in all_ivas:
                    if i_obj.porcentaje and float(i_obj.porcentaje) == 21.0:
                        client_iva_id = i_obj.id
                        break
            elif cond and "MONOTRIBUTO" in (cond.nombre or "").upper():
                iva_rate = 0.0
                for i_obj in all_ivas:
                    if i_obj.porcentaje and float(i_obj.porcentaje) == 0.0:
                        client_iva_id = i_obj.id
                        break
        
        # IIBB
        if client.condicion_iibb_id:
            # Add IIBB as a placeholder if configured
            # Note: We lost the specific 'alicuota' from ClienteImpuesto.
            # Assume 0 or 3% for now? 
            # Ideally we should add 'alicuota_iibb' to Cliente if we want to preserve this.
            pass

        # 3. Fetch Voucher
        voucher = await self.voucher_repo.get_by_id(voucher_id)
        if not voucher:
             raise ComprobanteNoEncontrado(f"Voucher {voucher_id} no encontrado en sistema externo.")

        # 4. Create Comprobante Payload
        detalles = []
        total_neto = voucher.monto_neto_ope
        total_iva = 0.0
        total_impuestos = 0.0
        impuestos = []
        
        # A. Taxable Portion (NetoOpe - NetoGSA)
        monto_imponible = voucher.monto_neto_ope - voucher.monto_neto_gsa
        if monto_imponible > 0:
            iva_amount = monto_imponible * (iva_rate / 100.0)
            total_iva += iva_amount
            
            detalles.append(ComprobanteDetalleCreate(
                comprobante_id=0,
                descripcion=f"{voucher.descripcion} (Servicios)",
                cantidad=1,
                precio_unitario=monto_imponible,
                importe=monto_imponible, 
                iva_id=client_iva_id,
                alicuota_iva=iva_rate,
                importe_iva=iva_amount,
                datos_extra={
                    "source_type": "voucher", 
                    "source_id": voucher.id, 
                    "voucher_nro": voucher.nro_voucher,
                    "sistema_origen": voucher.sistema_origen, 
                    "tipo_impositivo": "GRAVADO"
                }
            ))

        # B. Non-Taxable/Exempt Portion (NetoGSA)
        if voucher.monto_neto_gsa > 0:
            detalles.append(ComprobanteDetalleCreate(
                comprobante_id=0,
                descripcion=f"{voucher.descripcion} (No Gravado/GSA)",
                cantidad=1,
                precio_unitario=voucher.monto_neto_gsa,
                importe=voucher.monto_neto_gsa,
                iva_id=2, # Assuming 2 = 0% / Exento
                alicuota_iva=0.0,
                importe_iva=0.0,
                datos_extra={
                    "source_type": "voucher", 
                    "source_id": voucher.id, 
                    "voucher_nro": voucher.nro_voucher,
                    "sistema_origen": voucher.sistema_origen, 
                    "tipo_impositivo": "EXENTO"
                }
            ))

        # C. Impuestos (Taxes)
        if hasattr(voucher, 'monto_impuestos') and voucher.monto_impuestos > 0:
            total_impuestos += voucher.monto_impuestos
            impuestos.append(ComprobanteImpuestoCreate(
                comprobante_id=0, # Will be set by UOW
                tipo_impuesto_id=1, # Generic 'Otros' ID?
                descripcion="Impuestos Voucher (Externo)",
                base_imponible=0, # Unknown
                alicuota=0, 
                importe=voucher.monto_impuestos
            ))
            
        # D. Impuestos: From Client Configuration
        for tax_rule in other_taxes:
            if not tax_rule.aplica or tax_rule.alicuota is None or tax_rule.alicuota <= 0:
                continue
            
            # Resolve Base
            base_calculo_amount = 0.0
            tipo = await self.tipo_impuesto_repo.get_by_id(tax_rule.tipo_impuesto_id)
            if not tipo: continue

            # Default to NETO_GRAVADO if not specified or unknown
            base_enum = tipo.base_calculo if tipo.base_calculo else "neto_gravado"
            
            # Map Enum String to Value (Handle string or Enum object)
            base_str = str(base_enum).lower()
            
            if "subtotal" in base_str:
                base_calculo_amount = total_neto # Net Ope (Taxable + Exempt)
            elif "total" in base_str:
                # Circular dependency risk if we include current taxes. 
                # Usually means Net + IVA + Pre-existing taxes. 
                # For simplicity/safety: Net + IVA.
                base_calculo_amount = total_neto + total_iva 
            elif "otros" in base_str:
                base_calculo_amount = 0 # Define behavior for 'Otros'
            else: 
                # NETO_GRAVADO (Default)
                base_calculo_amount = monto_imponible

            tax_amount = base_calculo_amount * (tax_rule.alicuota / 100.0)
            
            if tax_amount > 0:
                total_impuestos += tax_amount
                impuestos.append(ComprobanteImpuestoCreate(
                    comprobante_id=0,
                    tipo_impuesto_id=tax_rule.tipo_impuesto_id if tax_rule.tipo_impuesto_id else 0,
                    descripcion=f"Impuesto Cliente ({tax_rule.alicuota}%) [{base_str}]",
                    base_imponible=base_calculo_amount,
                    alicuota=tax_rule.alicuota,
                    importe=tax_amount
                ))

        total_comprobante = total_neto + total_iva + total_impuestos

        from datetime import date
        
        payload = ComprobanteFullCreate(
            cliente_id=cliente_id,
            tipo_comprobante_id=tipo_comprobante_id,
            concepto_id=concepto_id,
            tipo_doc_id=99, # Consumidor Final
            moneda_id=1, # ARS
            punto_venta=punto_venta,
            fecha_emision=date.today(),
            cotizacion_moneda=1,
            # Mandatory fields required by Schema (Snapshot)
            numero=0, # Auto-generated
            doc_nro=client.cuit if client.cuit else "0", 
            nombre_cliente=f"{client.nombre or ''} {client.apellido or ''} {client.razon_social or ''}".strip() or "Consumidor Final",
            cuit_cliente=client.cuit if client.cuit else "00000000000",
            domicilio_cliente="Domicilio Cliente (Pendiente)", # To fetch if needed, but not critical for calculation now.
            localidad_cliente="Localidad (Pendiente)",
            cod_postal_cliente="0000",
            provincia_cliente="Provincia (Pendiente)",
            
            imputacion_credito_id=None,
            imputacion_debito_id=None,
            total_neto=total_neto,
            total_iva=total_iva,
            total_impuestos=total_impuestos,
            total=total_comprobante,
            moneda_cotizacion=1,
            detalles=detalles,
            impuestos=impuestos,
            observaciones=f"Facturación automática Voucher {voucher.nro_voucher}"
        )
        
        # 4. Save
        new_comprobante = await self.comprobante_use_case.create_comprobante_full(payload)
        
        return new_comprobante
