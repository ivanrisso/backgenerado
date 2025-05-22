from app.domain import *
from app.infrastructure.db.orm_models import *

# Map ORMs to Domain Entities

def orm_to_usuario(orm: Usuario) -> Usuario:
    return Usuario(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_rol(orm: Rol) -> Rol:
    return Rol(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_menuitem(orm: MenuItem) -> MenuItem:
    return MenuItem(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_cliente(orm: Cliente) -> Cliente:
    return Cliente(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_domicilio(orm: Domicilio) -> Domicilio:
    return Domicilio(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_telefono(orm: Telefono) -> Telefono:
    return Telefono(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_operador(orm: Operador) -> Operador:
    return Operador(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_tipodoc(orm: TipoDoc) -> TipoDoc:
    return TipoDoc(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_tipodom(orm: TipoDom) -> TipoDom:
    return TipoDom(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_tipotel(orm: TipoTel) -> TipoTel:
    return TipoTel(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_pais(orm: Pais) -> Pais:
    return Pais(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_provincia(orm: Provincia) -> Provincia:
    return Provincia(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_localidad(orm: Localidad) -> Localidad:
    return Localidad(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_tipocomprobante(orm: TipoComprobante) -> TipoComprobante:
    return TipoComprobante(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_concepto(orm: Concepto) -> Concepto:
    return Concepto(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_moneda(orm: Moneda) -> Moneda:
    return Moneda(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_iva(orm: Iva) -> Iva:
    return Iva(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_tipoimpuesto(orm: TipoImpuesto) -> TipoImpuesto:
    return TipoImpuesto(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_comprobante(orm: Comprobante) -> Comprobante:
    return Comprobante(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_comprobantedetalle(orm: ComprobanteDetalle) -> ComprobanteDetalle:
    return ComprobanteDetalle(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_comprobanteimpuesto(orm: ComprobanteImpuesto) -> ComprobanteImpuesto:
    return ComprobanteImpuesto(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_clienteimpuesto(orm: ClienteImpuesto) -> ClienteImpuesto:
    return ClienteImpuesto(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_cuentacorriente(orm: CuentaCorriente) -> CuentaCorriente:
    return CuentaCorriente(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


def orm_to_auditoriacomprobante(orm: AuditoriaComprobante) -> AuditoriaComprobante:
    return AuditoriaComprobante(**{k: getattr(orm, k) for k in orm.__table__.columns.keys()})


# Map Domain Entities to ORMs


def usuario_to_orm(domain: Usuario) -> Usuario:
    return Usuario(**domain.__dict__)


def rol_to_orm(domain: Rol) -> Rol:
    return Rol(**domain.__dict__)


def menuitem_to_orm(domain: MenuItem) -> MenuItem:
    return MenuItem(**domain.__dict__)


def cliente_to_orm(domain: Cliente) -> Cliente:
    return Cliente(**domain.__dict__)


def domicilio_to_orm(domain: Domicilio) -> Domicilio:
    return Domicilio(**domain.__dict__)


def telefono_to_orm(domain: Telefono) -> Telefono:
    return Telefono(**domain.__dict__)


def operador_to_orm(domain: Operador) -> Operador:
    return Operador(**domain.__dict__)


def tipodoc_to_orm(domain: TipoDoc) -> TipoDoc:
    return TipoDoc(**domain.__dict__)


def tipodom_to_orm(domain: TipoDom) -> TipoDom:
    return TipoDom(**domain.__dict__)


def tipotel_to_orm(domain: TipoTel) -> TipoTel:
    return TipoTel(**domain.__dict__)


def pais_to_orm(domain: Pais) -> Pais:
    return Pais(**domain.__dict__)


def provincia_to_orm(domain: Provincia) -> Provincia:
    return Provincia(**domain.__dict__)


def localidad_to_orm(domain: Localidad) -> Localidad:
    return Localidad(**domain.__dict__)


def tipocomprobante_to_orm(domain: TipoComprobante) -> TipoComprobante:
    return TipoComprobante(**domain.__dict__)


def concepto_to_orm(domain: Concepto) -> Concepto:
    return Concepto(**domain.__dict__)


def moneda_to_orm(domain: Moneda) -> Moneda:
    return Moneda(**domain.__dict__)


def iva_to_orm(domain: Iva) -> Iva:
    return Iva(**domain.__dict__)


def tipoimpuesto_to_orm(domain: TipoImpuesto) -> TipoImpuesto:
    return TipoImpuesto(**domain.__dict__)


def comprobante_to_orm(domain: Comprobante) -> Comprobante:
    return Comprobante(**domain.__dict__)


def comprobantedetalle_to_orm(domain: ComprobanteDetalle) -> ComprobanteDetalle:
    return ComprobanteDetalle(**domain.__dict__)


def comprobanteimpuesto_to_orm(domain: ComprobanteImpuesto) -> ComprobanteImpuesto:
    return ComprobanteImpuesto(**domain.__dict__)


def clienteimpuesto_to_orm(domain: ClienteImpuesto) -> ClienteImpuesto:
    return ClienteImpuesto(**domain.__dict__)


def cuentacorriente_to_orm(domain: CuentaCorriente) -> CuentaCorriente:
    return CuentaCorriente(**domain.__dict__)


def auditoriacomprobante_to_orm(domain: AuditoriaComprobante) -> AuditoriaComprobante:
    return AuditoriaComprobante(**domain.__dict__)