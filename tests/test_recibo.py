import pytest
from unittest.mock import MagicMock, AsyncMock
from datetime import date
from app.services.recibo_service import ReciboService
from app.schemas.recibo import ReciboCreate, ImputacionCreate
from app.domain.entities.comprobante import Comprobante
from app.domain.entities.tipocomprobante import TipoComprobante
from app.domain.entities.cliente import Cliente

@pytest.fixture
def mock_repos():
    return {
        "comprobante": AsyncMock(),
        "tipo": AsyncMock(),
        "imputacion": AsyncMock(),
        "cc": AsyncMock(),
        "cliente": AsyncMock()
    }

@pytest.fixture
def service(mock_repos):
    return ReciboService(
        mock_repos["comprobante"],
        mock_repos["tipo"],
        mock_repos["imputacion"],

        mock_repos["cc"],
        mock_repos["cliente"]
    )

@pytest.mark.asyncio
async def test_create_recibo_basic(service, mock_repos):
    # Setup Data
    mock_repos["tipo"].get_all.return_value = [
        TipoComprobante(id=1, codigo="RC", descripcion="Recibo", es_fiscal=False, codigo_arca="000")
    ]
    mock_repos["comprobante"].get_last_number.return_value = 100
    
    # Mock Recibo Created
    recibo_creado_mock = Comprobante(
        id=999, cliente_id=1, tipo_comprobante_id=1, concepto_id=1, tipo_doc_id=1, moneda_id=1,
        punto_venta=1, numero=101, fecha_emision=date.today(), doc_nro="", nombre_cliente="", cuit_cliente="",
        domicilio_cliente="", localidad_cliente="", cod_postal_cliente="", provincia_cliente="",
        cotizacion_moneda=1, total_neto=1000, total_iva=0, total_impuestos=0, total=1000, saldo=1000,
        observaciones="", cae="", cae_vencimiento=date.today()
    )
    mock_repos["comprobante"].create.return_value = recibo_creado_mock

    # Input
    data = ReciboCreate(
        cliente_id=1,
        fecha_emision=date.today(),
        punto_venta=1,
        total=1000,
        imputaciones=[]
    )

    # Act
    result = await service.create_recibo(data)

    # Assert
    assert result.id == 999
    assert result.numero == 101
    assert result.total == 1000
    assert result.saldo == 1000 # No imputations

    mock_repos["comprobante"].get_last_number.assert_called_with(1, 1)
    mock_repos["comprobante"].create.assert_called_once()

    mock_repos["cc"].create.assert_called_once() # Verify CC movement creation
    mock_repos["cliente"].get_by_id.assert_called_once()

@pytest.mark.asyncio
async def test_create_recibo_with_imputation(service, mock_repos):
    # Setup Tipo
    mock_repos["tipo"].get_all.return_value = [
        TipoComprobante(id=1, codigo="RC", descripcion="Recibo", es_fiscal=False, codigo_arca="000")
    ]
    mock_repos["comprobante"].get_last_number.return_value = 100

    # Setup Invoice to Pay
    invoice = Comprobante(
        id=50, cliente_id=1, tipo_comprobante_id=2, concepto_id=1, tipo_doc_id=1, moneda_id=1,
        punto_venta=1, numero=200, fecha_emision=date.today(), doc_nro="", nombre_cliente="", cuit_cliente="",
        domicilio_cliente="", localidad_cliente="", cod_postal_cliente="", provincia_cliente="",
        cotizacion_moneda=1, total_neto=2000, total_iva=0, total_impuestos=0, total=2000, saldo=2000, # Full Balance
        observaciones="", cae="123", cae_vencimiento=date.today()
    )
    mock_repos["comprobante"].get_by_id.return_value = invoice

    # Mock Recibo Create (Initial)
    recibo_creado_mock = Comprobante(
        id=999, cliente_id=1, tipo_comprobante_id=1, concepto_id=1, tipo_doc_id=1, moneda_id=1,
        punto_venta=1, numero=101, fecha_emision=date.today(), doc_nro="", nombre_cliente="", cuit_cliente="",
        domicilio_cliente="", localidad_cliente="", cod_postal_cliente="", provincia_cliente="",
        cotizacion_moneda=1, total_neto=1000, total_iva=0, total_impuestos=0, total=1000, saldo=1000, # Initial
        observaciones="", cae="", cae_vencimiento=date.today()
    )
    mock_repos["comprobante"].create.return_value = recibo_creado_mock

    # Mock Cliente
    cliente_mock = Cliente(
        id=1, tipo_doc_id=99, cuit="20123456789", razon_social="Cliente Test",
        nombre="Cliente", apellido="Test", email="test@cliente.com"
    )
    mock_repos["cliente"].get_by_id.return_value = cliente_mock

    # Input: Pay 1000 out of 2000 debt
    data = ReciboCreate(
        cliente_id=1,
        fecha_emision=date.today(),
        punto_venta=1,
        total=1000,
        imputaciones=[
            ImputacionCreate(comprobante_deuda_id=50, importe=1000)
        ]
    )

    # Act
    result = await service.create_recibo(data)

    # Assert
    # 1. Invoice updated
    assert invoice.saldo == 1000 # 2000 - 1000
    mock_repos["comprobante"].update.assert_any_call(50, invoice, commit=False)

    # 2. Imputation Created
    mock_repos["imputacion"].create.assert_called_once()
    
    
    # 3. Recibo Updated (final balance 0 because fully applied)
    assert recibo_creado_mock.saldo == 0
    mock_repos["comprobante"].update.assert_any_call(999, recibo_creado_mock, commit=True)

