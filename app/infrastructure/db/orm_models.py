from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, DateTime, Text, Numeric
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from enum import Enum
from app.domain.entities.enums import TipoAplicacionEnum, BaseTributarioEnum

class Base(DeclarativeBase):
    pass


class RolesUsuario(Base):
    __tablename__ = "rolesusuario"

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), primary_key=True)
    rol_id: Mapped[int] = mapped_column(ForeignKey("rol.id"), primary_key=True)


class RolMenuItem(Base):
    __tablename__ = "rolmenuitem"

    rol_id: Mapped[int] = mapped_column(ForeignKey("rol.id"), primary_key=True)
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menuitem.id"), primary_key=True)


class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    usuario_password: Mapped[str] = mapped_column(String(100), nullable=False)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)
    apellido: Mapped[str] = mapped_column(String(30), nullable=False)

    roles: Mapped[List["Rol"]] = relationship(secondary="rolesusuario", back_populates="usuarios")
    auditorias: Mapped[List["AuditoriaComprobante"]] = relationship(back_populates="usuario")


class Rol(Base):
    __tablename__ = "rol"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rol_nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    es_admin: Mapped[bool] = mapped_column(nullable=False)

    usuarios: Mapped[List["Usuario"]] = relationship(secondary="rolesusuario", back_populates="roles")
    menuitems: Mapped[List["MenuItem"]] = relationship(secondary="rolmenuitem", back_populates="roles")


class MenuItem(Base):
    __tablename__ = "menuitem"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    path: Mapped[Optional[str]] = mapped_column(String(200))
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("menuitem.id"))

    parent: Mapped[Optional["MenuItem"]] = relationship(back_populates="children", remote_side="MenuItem.id")
    children: Mapped[List["MenuItem"]] = relationship(back_populates="parent")

    roles: Mapped[List["Rol"]] = relationship(secondary="rolmenuitem", back_populates="menuitems")

    

class TipoDoc(Base):
    __tablename__ = "tipodoc"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tipo_doc_nombre: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    habilitado: Mapped[bool] = mapped_column(nullable=False)

    comprobantes: Mapped[List["Comprobante"]] = relationship(back_populates="tipo_doc")
    clientes: Mapped[List["Cliente"]] = relationship(back_populates="tipo_doc")
    
class TipoDom(Base):
    __tablename__ = "tipodom"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)

    domicilios: Mapped[List["Domicilio"]] = relationship(back_populates="tipo_dom")
    
    
class TipoTel(Base):
    __tablename__ = "tipotel"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)

    telefonos: Mapped[List["Telefono"]] = relationship(back_populates="tipo_tel")
    
    
class Pais(Base):
    __tablename__ = "pais"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(2), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)

    provincias: Mapped[List["Provincia"]] = relationship(back_populates="pais")


class Provincia(Base):
    __tablename__ = "provincia"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    provincia_nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    pais_id: Mapped[int] = mapped_column(ForeignKey("pais.id"), nullable=False)

    pais: Mapped["Pais"] = relationship(back_populates="provincias")
    localidades: Mapped[List["Localidad"]] = relationship(back_populates="provincia")


class Localidad(Base):
    __tablename__ = "localidad"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    localidad_nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    cod_postal: Mapped[str] = mapped_column(String(15), nullable=False)
    provincia_id: Mapped[int] = mapped_column(ForeignKey("provincia.id"), nullable=False)

    provincia: Mapped["Provincia"] = relationship(back_populates="localidades")
    domicilios: Mapped[List["Domicilio"]] = relationship(back_populates="localidad")

    

class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    apellido: Mapped[str] = mapped_column(String(50), nullable=False)
    razon_social: Mapped[Optional[str]] = mapped_column(String(100))
    cuit: Mapped[Optional[str]] = mapped_column(String(11), unique=True)
    email: Mapped[Optional[str]] = mapped_column(String(100))

    tipo_doc_id: Mapped[int] = mapped_column(ForeignKey("tipodoc.id"), nullable=False)
    iva_id: Mapped[int] = mapped_column(ForeignKey("iva.id"), nullable=False)

    tipo_doc: Mapped["TipoDoc"] = relationship(back_populates="clientes")
    iva: Mapped["Iva"] = relationship(back_populates="clientes")

    comprobantes: Mapped[List["Comprobante"]] = relationship(back_populates="cliente")
    domicilios: Mapped[List["Domicilio"]] = relationship(back_populates="cliente")
    impuestos: Mapped[List["ClienteImpuesto"]] = relationship(back_populates="cliente")
    movimientos_cc: Mapped[List["CuentaCorriente"]] = relationship(back_populates="cliente")
    operadores: Mapped[List["Operador"]] = relationship(back_populates="cliente")
    
    
class Domicilio(Base):
    __tablename__ = "domicilio"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    calle: Mapped[str] = mapped_column(String(60), nullable=False)
    numero: Mapped[int] = mapped_column(nullable=False)

    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"), nullable=False)
    tipo_dom_id: Mapped[int] = mapped_column(ForeignKey("tipodom.id"), nullable=False)
    localidad_id: Mapped[int] = mapped_column(ForeignKey("localidad.id"), nullable=False)

    cliente: Mapped["Cliente"] = relationship(back_populates="domicilios")
    tipo_dom: Mapped["TipoDom"] = relationship(back_populates="domicilios")
    localidad: Mapped["Localidad"] = relationship(back_populates="domicilios")

    telefonos: Mapped[List["Telefono"]] = relationship(back_populates="domicilio")
    
    
class Telefono(Base):
    __tablename__ = "telefono"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tipo_tel_id: Mapped[int] = mapped_column(ForeignKey("tipotel.id"), nullable=False)
    prefijo: Mapped[str] = mapped_column(String(10), nullable=False)
    numero: Mapped[str] = mapped_column(String(12), nullable=False)
    domicilio_id: Mapped[int] = mapped_column(ForeignKey("domicilio.id"), nullable=False)

    tipo_tel: Mapped["TipoTel"] = relationship(back_populates="telefonos")
    domicilio: Mapped["Domicilio"] = relationship(back_populates="telefonos")
    
class Operador(Base):
    __tablename__ = "operador"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"), nullable=False)

    cliente: Mapped["Cliente"] = relationship(back_populates="operadores")




class TipoComprobante(Base):
    __tablename__ = "tipocomprobante"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(3), nullable=False, unique=True)
    descripcion: Mapped[str] = mapped_column(String(50), nullable=False)
    es_fiscal: Mapped[bool] = mapped_column(nullable=False)

    comprobantes: Mapped[List["Comprobante"]] = relationship(back_populates="tipo_comprobante")

class Concepto(Base):
    __tablename__ = "concepto"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(3), nullable=False, unique=True)
    descripcion: Mapped[str] = mapped_column(String(50), nullable=False)

    comprobantes: Mapped[List["Comprobante"]] = relationship(back_populates="concepto")

class Moneda(Base):
    __tablename__ = "moneda"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(3), nullable=False, unique=True)
    descripcion: Mapped[str] = mapped_column(String(50), nullable=False)

    comprobantes: Mapped[List["Comprobante"]] = relationship(back_populates="moneda")

class Iva(Base):
    __tablename__ = "iva"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[int] = mapped_column(unique=True, index=True, nullable=False)
    descripcion: Mapped[str] = mapped_column(String(30), nullable=False)
    porcentaje: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=Decimal("0.00"))
    discriminado: Mapped[bool] = mapped_column(nullable=False, default=False)
    porcentaje_sobre: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=Decimal("0.00"))

    clientes: Mapped[List["Cliente"]] = relationship(back_populates="iva")
    detalles: Mapped[List["ComprobanteDetalle"]] = relationship(back_populates="iva")

class TipoImpuesto(Base):
    __tablename__ = "tipoimpuesto"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo_afip: Mapped[str] = mapped_column(String(3), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(20), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo_aplicacion: Mapped[TipoAplicacionEnum] = mapped_column(nullable=False)
    base_calculo: Mapped[BaseTributarioEnum] = mapped_column(nullable=False)
    porcentaje: Mapped[Optional[float]] = mapped_column()
    editable: Mapped[bool] = mapped_column(nullable=False, default=True)
    obligatorio: Mapped[bool] = mapped_column(nullable=False, default=False)
    activo: Mapped[bool] = mapped_column(nullable=False, default=True)

    clientes: Mapped[List["ClienteImpuesto"]] = relationship(back_populates="tipo_impuesto")
    comprobantes: Mapped[List["ComprobanteImpuesto"]] = relationship(back_populates="tipo_impuesto")
    
    
class Comprobante(Base):
    __tablename__ = "comprobante"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"), nullable=False)
    tipo_comprobante_id: Mapped[int] = mapped_column(ForeignKey("tipocomprobante.id"), nullable=False)
    concepto_id: Mapped[int] = mapped_column(ForeignKey("concepto.id"), nullable=False)
    tipo_doc_id: Mapped[int] = mapped_column(ForeignKey("tipodoc.id"), nullable=False)
    moneda_id: Mapped[int] = mapped_column(ForeignKey("moneda.id"), nullable=False)

    punto_venta: Mapped[int] = mapped_column(nullable=False)
    numero: Mapped[int] = mapped_column(nullable=False, unique=True)
    fecha_emision: Mapped[date] = mapped_column(nullable=False)

    doc_nro: Mapped[str] = mapped_column(String(20), nullable=False)
    nombre_cliente: Mapped[str] = mapped_column(String(100), nullable=False)
    cuit_cliente: Mapped[str] = mapped_column(String(20), nullable=False)
    domicilio_cliente: Mapped[str] = mapped_column(String(100), nullable=False)
    localidad_cliente: Mapped[str] = mapped_column(String(50), nullable=False)
    cod_postal_cliente: Mapped[Optional[str]] = mapped_column(String(10))
    provincia_cliente: Mapped[str] = mapped_column(String(50), nullable=False)

    cotizacion_moneda: Mapped[float] = mapped_column(nullable=False)
    total_neto: Mapped[float] = mapped_column(nullable=False)
    total_iva: Mapped[float] = mapped_column(nullable=False)
    total_impuestos: Mapped[float] = mapped_column(nullable=False)
    total: Mapped[float] = mapped_column(nullable=False)
    observaciones: Mapped[Optional[str]] = mapped_column(String(255))

    tipo_comprobante: Mapped["TipoComprobante"] = relationship(back_populates="comprobantes")
    concepto: Mapped["Concepto"] = relationship(back_populates="comprobantes")
    tipo_doc: Mapped["TipoDoc"] = relationship(back_populates="comprobantes")
    moneda: Mapped["Moneda"] = relationship(back_populates="comprobantes")
    cliente: Mapped["Cliente"] = relationship(back_populates="comprobantes")

    detalles: Mapped[List["ComprobanteDetalle"]] = relationship(back_populates="comprobante")
    impuestos: Mapped[List["ComprobanteImpuesto"]] = relationship(back_populates="comprobante")
    registro_cc: Mapped[Optional["CuentaCorriente"]] = relationship(back_populates="comprobante")
    auditorias: Mapped[List["AuditoriaComprobante"]] = relationship(back_populates="comprobante")


class ComprobanteDetalle(Base):
    __tablename__ = "comprobantedetalle"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    comprobante_id: Mapped[int] = mapped_column(ForeignKey("comprobante.id"), nullable=False)
    iva_id: Mapped[int] = mapped_column(ForeignKey("iva.id"), nullable=False)

    descripcion: Mapped[str] = mapped_column(String(200), nullable=False)
    cantidad: Mapped[float] = mapped_column(nullable=False)
    precio_unitario: Mapped[float] = mapped_column(nullable=False)
    importe: Mapped[float] = mapped_column(nullable=False)
    alicuota_iva: Mapped[float] = mapped_column(nullable=False)
    importe_iva: Mapped[float] = mapped_column(nullable=False)

    comprobante: Mapped["Comprobante"] = relationship(back_populates="detalles")
    iva: Mapped["Iva"] = relationship(back_populates="detalles")


class ComprobanteImpuesto(Base):
    __tablename__ = "comprobanteimpuesto"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    comprobante_id: Mapped[int] = mapped_column(ForeignKey("comprobante.id"), nullable=False)
    tipo_impuesto_id: Mapped[int] = mapped_column(ForeignKey("tipoimpuesto.id"), nullable=False)

    descripcion: Mapped[str] = mapped_column(String(100), nullable=False)
    base_imponible: Mapped[float] = mapped_column(nullable=False)
    alicuota: Mapped[float] = mapped_column(nullable=False)
    importe: Mapped[float] = mapped_column(nullable=False)

    comprobante: Mapped["Comprobante"] = relationship(back_populates="impuestos")
    tipo_impuesto: Mapped["TipoImpuesto"] = relationship(back_populates="comprobantes")

    
class ClienteImpuesto(Base):
    __tablename__ = "clienteimpuesto"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"), nullable=False)
    tipo_impuesto_id: Mapped[int] = mapped_column(ForeignKey("tipoimpuesto.id"), nullable=False)

    aplica: Mapped[bool] = mapped_column(default=True, nullable=False)
    alicuota: Mapped[Optional[float]] = mapped_column()
    observaciones: Mapped[Optional[str]] = mapped_column(String(255))

    cliente: Mapped["Cliente"] = relationship(back_populates="impuestos")
    tipo_impuesto: Mapped["TipoImpuesto"] = relationship(back_populates="clientes")
    
class CuentaCorriente(Base):
    __tablename__ = "cuentacorriente"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"), nullable=False)
    comprobante_id: Mapped[Optional[int]] = mapped_column(ForeignKey("comprobante.id"))

    fecha: Mapped[date] = mapped_column(nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255))
    importe: Mapped[float] = mapped_column(nullable=False)
    signo: Mapped[int] = mapped_column(nullable=False)
    saldo: Mapped[Optional[float]] = mapped_column()

    cliente: Mapped["Cliente"] = relationship(back_populates="movimientos_cc")
    comprobante: Mapped[Optional["Comprobante"]] = relationship(back_populates="registro_cc")


class AuditoriaComprobante(Base):
    __tablename__ = "auditoriacomprobante"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    comprobante_id: Mapped[int] = mapped_column(ForeignKey("comprobante.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)

    accion: Mapped[str] = mapped_column(String(20), nullable=False)
    detalle: Mapped[Optional[str]] = mapped_column(String(255))
    ip_origen: Mapped[Optional[str]] = mapped_column(String(50))
    fecha: Mapped[datetime] = mapped_column(nullable=False)

    comprobante: Mapped["Comprobante"] = relationship(back_populates="auditorias")
    usuario: Mapped["Usuario"] = relationship(back_populates="auditorias")

