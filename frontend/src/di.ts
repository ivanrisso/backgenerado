import { AxiosAuthRepository } from '@infra/repositories/AxiosAuthRepository';
import { AxiosClienteRepository } from '@infra/repositories/AxiosClienteRepository';
import { AxiosComprobanteRepository } from '@infra/repositories/AxiosComprobanteRepository';

// New Infrastructure Imports
import { AxiosTipoDocRepository } from '@infra/repositories/AxiosTipoDocRepository';
import { AxiosPaisRepository } from '@infra/repositories/AxiosPaisRepository';
import { AxiosProvinciaRepository } from '@infra/repositories/AxiosProvinciaRepository';
import { AxiosLocalidadRepository } from '@infra/repositories/AxiosLocalidadRepository';
import { AxiosTipoDomRepository } from '@infra/repositories/AxiosTipoDomRepository';
import { AxiosTipoTelRepository } from '@infra/repositories/AxiosTipoTelRepository';
import { HttpCondicionTributariaRepository } from '@infra/repositories/HttpCondicionTributariaRepository';



import { GetClientesUseCase } from '@modules/Clientes/application/GetClientesUseCase';
import { CreateClienteUseCase } from '@modules/Clientes/application/CreateClienteUseCase';
import { UpdateClienteUseCase } from '@modules/Clientes/application/UpdateClienteUseCase';
import { GetClienteByIdUseCase } from '@modules/Clientes/application/GetClienteByIdUseCase';
import { DeleteClienteUseCase } from '@modules/Clientes/application/DeleteClienteUseCase';
import { GetAfipTaxComparisonUseCase } from '@modules/Facturacion/application/GetAfipTaxComparisonUseCase';
import { SyncAfipTaxesUseCase } from '@modules/Facturacion/application/SyncAfipTaxesUseCase';
import { GetCondicionesTributariasUseCase } from '@modules/Maestros/application/condiciontributaria/GetCondicionesTributariasUseCase';



import { GetComprobantesUseCase } from '@modules/Facturacion/application/GetComprobantesUseCase';
import { CreateComprobanteUseCase } from '@modules/Facturacion/application/CreateComprobanteUseCase';

import { LoginUseCase } from '@modules/Auth/application/LoginUseCase';
import { LogoutUseCase } from '@modules/Auth/application/LogoutUseCase';
import { GetProfileUseCase } from '@modules/Auth/application/GetProfileUseCase';

// New UseCase Imports
import { GetTiposDocUseCase } from '@modules/Maestros/application/TipoDoc/GetTiposDocUseCase';
import { GetTipoDocByIdUseCase } from '@modules/Maestros/application/TipoDoc/GetTipoDocByIdUseCase';
import { CreateTipoDocUseCase } from '@modules/Maestros/application/TipoDoc/CreateTipoDocUseCase';
import { UpdateTipoDocUseCase } from '@modules/Maestros/application/TipoDoc/UpdateTipoDocUseCase';
import { DeleteTipoDocUseCase } from '@modules/Maestros/application/TipoDoc/DeleteTipoDocUseCase';

import { GetPaisesUseCase } from '@modules/Maestros/application/Pais/GetPaisesUseCase';
import { CreatePaisUseCase } from '@modules/Maestros/application/Pais/CreatePaisUseCase';
import { UpdatePaisUseCase } from '@modules/Maestros/application/Pais/UpdatePaisUseCase';
import { DeletePaisUseCase } from '@modules/Maestros/application/Pais/DeletePaisUseCase';

import { GetProvinciasByPaisUseCase } from '@modules/Maestros/application/Provincia/GetProvinciasByPaisUseCase';
import { CreateProvinciaUseCase } from '@modules/Maestros/application/Provincia/CreateProvinciaUseCase';
import { UpdateProvinciaUseCase } from '@modules/Maestros/application/Provincia/UpdateProvinciaUseCase';
import { DeleteProvinciaUseCase } from '@modules/Maestros/application/Provincia/DeleteProvinciaUseCase';

import { GetLocalidadesByProvinciaUseCase } from '@modules/Maestros/application/Localidad/GetLocalidadesByProvinciaUseCase';
import { CreateLocalidadUseCase } from '@modules/Maestros/application/Localidad/CreateLocalidadUseCase';
import { UpdateLocalidadUseCase } from '@modules/Maestros/application/Localidad/UpdateLocalidadUseCase';
import { DeleteLocalidadUseCase } from '@modules/Maestros/application/Localidad/DeleteLocalidadUseCase';

import { GetTiposDomUseCase } from '@modules/Maestros/application/TipoDom/GetTiposDomUseCase';
import { CreateTipoDomUseCase } from '@modules/Maestros/application/TipoDom/CreateTipoDomUseCase';
import { UpdateTipoDomUseCase } from '@modules/Maestros/application/TipoDom/UpdateTipoDomUseCase';
import { DeleteTipoDomUseCase } from '@modules/Maestros/application/TipoDom/DeleteTipoDomUseCase';

import { GetTiposTelUseCase } from '@modules/Maestros/application/TipoTel/GetTiposTelUseCase';
import { CreateTipoTelUseCase } from '@modules/Maestros/application/TipoTel/CreateTipoTelUseCase';
import { UpdateTipoTelUseCase } from '@modules/Maestros/application/TipoTel/UpdateTipoTelUseCase';
import { DeleteTipoTelUseCase } from '@modules/Maestros/application/TipoTel/DeleteTipoTelUseCase';

import { GetLocalidadByIdUseCase } from '@modules/Maestros/application/ubicacion/GetLocalidadByIdUseCase';
import { GetProvinciaByIdUseCase } from '@modules/Maestros/application/ubicacion/GetProvinciaByIdUseCase';
// Auth & RBAC Imports
import { AxiosUsuarioRepository } from '@infra/repositories/AxiosUsuarioRepository';
import { AxiosRolRepository } from '@infra/repositories/AxiosRolRepository';
import { AxiosMenuItemRepository } from '@infra/repositories/AxiosMenuItemRepository';
import { AxiosAuthService } from '@infra/services/AxiosAuthService';


/*
import {
    GetAllUsuariosUseCase,
    GetUsuarioByIdUseCase,
    CreateUsuarioUseCase,
    UpdateUsuarioUseCase,
    DeleteUsuarioUseCase,
    AssignRolesToUsuarioUseCase
} from '@app/usecases/usuario/UsuarioUseCases';

import {
    GetAllRolesUseCase,
    GetRolByIdUseCase,
    CreateRolUseCase,
    UpdateRolUseCase,
    DeleteRolUseCase
} from '@app/usecases/rol/RolUseCases';

import {
    GetMenuTreeUseCase,
    CreateMenuItemUseCase,
    UpdateMenuItemUseCase,
    DeleteMenuItemUseCase,
    AssignRolesToMenuItemUseCase
} from '@app/usecases/menuitem/MenuItemUseCases';
*/

// import { AuthUseCase } from '@modules/Auth/application/AuthUseCase';

// ... existing imports ...
import { HttpDomicilioRepository } from '@infra/repositories/HttpDomicilioRepository';
import { HttpTelefonoRepository } from '@infra/repositories/HttpTelefonoRepository';
import { HttpOperadorRepository } from '@infra/repositories/HttpOperadorRepository';
import { HttpTipoComprobanteRepository } from '@infra/repositories/HttpTipoComprobanteRepository';
import { HttpConceptoRepository } from '@infra/repositories/HttpConceptoRepository';
import { HttpMonedaRepository } from '@infra/repositories/HttpMonedaRepository';
import { HttpIvaRepository } from '@infra/repositories/HttpIvaRepository';
import { HttpTipoImpuestoRepository } from '@infra/repositories/HttpTipoImpuestoRepository';
import { HttpArticuloRepository } from '@infra/repositories/HttpArticuloRepository';

import { GetArticulosUseCase } from '@modules/Maestros/application/articulo/GetArticulosUseCase';
import { CreateArticuloUseCase } from '@modules/Maestros/application/articulo/CreateArticuloUseCase';
import { UpdateArticuloUseCase } from '@modules/Maestros/application/articulo/UpdateArticuloUseCase';
import { DeleteArticuloUseCase } from '@modules/Maestros/application/articulo/DeleteArticuloUseCase';

import { GetDomiciliosUseCase } from '@modules/Maestros/application/domicilio/GetDomiciliosUseCase';
import { CreateDomicilioUseCase } from '@modules/Maestros/application/domicilio/CreateDomicilioUseCase';
import { UpdateDomicilioUseCase } from '@modules/Maestros/application/domicilio/UpdateDomicilioUseCase';
import { DeleteDomicilioUseCase } from '@modules/Maestros/application/domicilio/DeleteDomicilioUseCase';
import { GetDomicilioByIdUseCase } from '@modules/Maestros/application/domicilio/GetDomicilioByIdUseCase';

import { GetTelefonosUseCase } from '@modules/Maestros/application/telefono/GetTelefonosUseCase';
import { CreateTelefonoUseCase } from '@modules/Maestros/application/telefono/CreateTelefonoUseCase';
import { UpdateTelefonoUseCase } from '@modules/Maestros/application/telefono/UpdateTelefonoUseCase';
import { DeleteTelefonoUseCase } from '@modules/Maestros/application/telefono/DeleteTelefonoUseCase';

import { GetOperadoresUseCase } from '@modules/Maestros/application/operador/GetOperadoresUseCase';
import { CreateOperadorUseCase } from '@modules/Maestros/application/operador/CreateOperadorUseCase';
import { DeleteOperadorUseCase } from '@modules/Maestros/application/operador/DeleteOperadorUseCase';

import { GetTiposComprobanteUseCase } from '@modules/Maestros/application/tipocomprobante/GetTiposComprobanteUseCase';
import { GetConceptosUseCase } from '@modules/Maestros/application/concepto/GetConceptosUseCase';
import { GetMonedasUseCase } from '@modules/Maestros/application/moneda/GetMonedasUseCase';
import { GetIvasUseCase } from '@modules/Maestros/application/iva/GetIvasUseCase';

import { GetTiposImpuestoUseCase } from '@modules/Maestros/application/tipoimpuesto/GetTiposImpuestoUseCase';
import { CreateTipoImpuestoUseCase } from '@modules/Maestros/application/tipoimpuesto/CreateTipoImpuestoUseCase';
import { UpdateTipoImpuestoUseCase } from '@modules/Maestros/application/tipoimpuesto/UpdateTipoImpuestoUseCase';
import { DeleteTipoImpuestoUseCase } from '@modules/Maestros/application/tipoimpuesto/DeleteTipoImpuestoUseCase';
import { CreateIvaUseCase } from '@modules/Maestros/application/iva/CreateIvaUseCase';
import { UpdateIvaUseCase } from '@modules/Maestros/application/iva/UpdateIvaUseCase';
import { DeleteIvaUseCase } from '@modules/Maestros/application/iva/DeleteIvaUseCase';


import { CreateMonedaUseCase } from '@modules/Maestros/application/moneda/CreateMonedaUseCase';

import { UpdateMonedaUseCase } from '@modules/Maestros/application/moneda/UpdateMonedaUseCase';
import { DeleteMonedaUseCase } from '@modules/Maestros/application/moneda/DeleteMonedaUseCase';

import { CreateConceptoUseCase } from '@modules/Maestros/application/concepto/CreateConceptoUseCase';
import { UpdateConceptoUseCase } from '@modules/Maestros/application/concepto/UpdateConceptoUseCase';
import { DeleteConceptoUseCase } from '@modules/Maestros/application/concepto/DeleteConceptoUseCase';

import { CreateTipoComprobanteUseCase } from '@modules/Maestros/application/tipocomprobante/CreateTipoComprobanteUseCase';
import { UpdateTipoComprobanteUseCase } from '@modules/Maestros/application/tipocomprobante/UpdateTipoComprobanteUseCase';
import { DeleteTipoComprobanteUseCase } from '@modules/Maestros/application/tipocomprobante/DeleteTipoComprobanteUseCase';

import { UpdateOperadorUseCase } from '@modules/Maestros/application/operador/UpdateOperadorUseCase';
import { AxiosComprobanteFullRepository } from '@infra/repositories/AxiosComprobanteFullRepository';
import { CreateComprobanteFullUseCase } from '@modules/Facturacion/application/CreateComprobanteFullUseCase';

import { CreateCondicionTributariaUseCase } from '@modules/Maestros/application/condiciontributaria/CreateCondicionTributariaUseCase';
import { UpdateCondicionTributariaUseCase } from '@modules/Maestros/application/condiciontributaria/UpdateCondicionTributariaUseCase';
import { DeleteCondicionTributariaUseCase } from '@modules/Maestros/application/condiciontributaria/DeleteCondicionTributariaUseCase';

// Repositories
const authRepository = new AxiosAuthRepository();
const clienteRepository = new AxiosClienteRepository();
const comprobanteRepository = new AxiosComprobanteRepository();

// New Repositories
const tipoDocRepository = new AxiosTipoDocRepository();
const paisRepository = new AxiosPaisRepository();
const provinciaRepository = new AxiosProvinciaRepository();
const localidadRepository = new AxiosLocalidadRepository();
const tipoDomRepository = new AxiosTipoDomRepository();
const tipoTelRepository = new AxiosTipoTelRepository();
const condicionTributariaRepository = new HttpCondicionTributariaRepository();


// Use Cases
export const getClientesUseCase = new GetClientesUseCase(clienteRepository);
export const createClienteUseCase = new CreateClienteUseCase(clienteRepository);
export const updateClienteUseCase = new UpdateClienteUseCase(clienteRepository);
export const getClienteByIdUseCase = new GetClienteByIdUseCase(clienteRepository);
export const deleteClienteUseCase = new DeleteClienteUseCase(clienteRepository);
export const getAfipTaxComparisonUseCase = new GetAfipTaxComparisonUseCase(clienteRepository);
export const syncAfipTaxesUseCase = new SyncAfipTaxesUseCase(clienteRepository);


export const getComprobantesUseCase = new GetComprobantesUseCase(comprobanteRepository);
export const createComprobanteUseCase = new CreateComprobanteUseCase(comprobanteRepository);

export const loginUseCase = new LoginUseCase(authRepository);
export const logoutUseCase = new LogoutUseCase(authRepository);
export const getProfileUseCase = new GetProfileUseCase(authRepository);

// New UseCase Exports
export const getTiposDocUseCase = new GetTiposDocUseCase(tipoDocRepository);
export const getTipoDocByIdUseCase = new GetTipoDocByIdUseCase(tipoDocRepository);
export const createTipoDocUseCase = new CreateTipoDocUseCase(tipoDocRepository);
export const updateTipoDocUseCase = new UpdateTipoDocUseCase(tipoDocRepository);
export const deleteTipoDocUseCase = new DeleteTipoDocUseCase(tipoDocRepository);

// ... existing code ...
export const getLocalidadByIdUseCase = new GetLocalidadByIdUseCase(localidadRepository);
export const getProvinciaByIdUseCase = new GetProvinciaByIdUseCase(provinciaRepository);
export const getPaisesUseCase = new GetPaisesUseCase(paisRepository);
export const createPaisUseCase = new CreatePaisUseCase(paisRepository);
export const updatePaisUseCase = new UpdatePaisUseCase(paisRepository);
export const deletePaisUseCase = new DeletePaisUseCase(paisRepository);

export const getProvinciasByPaisUseCase = new GetProvinciasByPaisUseCase(provinciaRepository);
export const createProvinciaUseCase = new CreateProvinciaUseCase(provinciaRepository);
export const updateProvinciaUseCase = new UpdateProvinciaUseCase(provinciaRepository);
export const deleteProvinciaUseCase = new DeleteProvinciaUseCase(provinciaRepository);

export const getLocalidadesByProvinciaUseCase = new GetLocalidadesByProvinciaUseCase(localidadRepository);
export const createLocalidadUseCase = new CreateLocalidadUseCase(localidadRepository);
export const updateLocalidadUseCase = new UpdateLocalidadUseCase(localidadRepository);
export const deleteLocalidadUseCase = new DeleteLocalidadUseCase(localidadRepository);

export const getTiposDomUseCase = new GetTiposDomUseCase(tipoDomRepository);
export const createTipoDomUseCase = new CreateTipoDomUseCase(tipoDomRepository);
export const updateTipoDomUseCase = new UpdateTipoDomUseCase(tipoDomRepository);
export const deleteTipoDomUseCase = new DeleteTipoDomUseCase(tipoDomRepository);

export const getTiposTelUseCase = new GetTiposTelUseCase(tipoTelRepository);
export const createTipoTelUseCase = new CreateTipoTelUseCase(tipoTelRepository);
export const updateTipoTelUseCase = new UpdateTipoTelUseCase(tipoTelRepository);
export const deleteTipoTelUseCase = new DeleteTipoTelUseCase(tipoTelRepository);

// ... existing imports ...

// RBAC Repositories
const usuarioRepository = new AxiosUsuarioRepository();
const rolRepository = new AxiosRolRepository();
const menuItemRepository = new AxiosMenuItemRepository();
const authService = new AxiosAuthService(); // Service, not Repository in strict sense but fulfills interface

// Auth Use Case
// export const authUseCase = new AuthUseCase(authService);

/*
// Usuario Use Cases
export const getAllUsuariosUseCase = new GetAllUsuariosUseCase(usuarioRepository);
export const getUsuarioByIdUseCase = new GetUsuarioByIdUseCase(usuarioRepository);
export const createUsuarioUseCase = new CreateUsuarioUseCase(usuarioRepository);
export const updateUsuarioUseCase = new UpdateUsuarioUseCase(usuarioRepository);
export const deleteUsuarioUseCase = new DeleteUsuarioUseCase(usuarioRepository);
export const assignRolesToUsuarioUseCase = new AssignRolesToUsuarioUseCase(usuarioRepository);

// Rol Use Cases
export const getAllRolesUseCase = new GetAllRolesUseCase(rolRepository);
export const getRolByIdUseCase = new GetRolByIdUseCase(rolRepository);
export const createRolUseCase = new CreateRolUseCase(rolRepository);
export const updateRolUseCase = new UpdateRolUseCase(rolRepository);
export const deleteRolUseCase = new DeleteRolUseCase(rolRepository);

// MenuItem Use Cases
export const getMenuTreeUseCase = new GetMenuTreeUseCase(menuItemRepository);
export const createMenuItemUseCase = new CreateMenuItemUseCase(menuItemRepository);
export const updateMenuItemUseCase = new UpdateMenuItemUseCase(menuItemRepository);
export const deleteMenuItemUseCase = new DeleteMenuItemUseCase(menuItemRepository);
export const assignRolesToMenuItemUseCase = new AssignRolesToMenuItemUseCase(menuItemRepository);
*/

const domicilioRepository = new HttpDomicilioRepository();
const telefonoRepository = new HttpTelefonoRepository();
const operadorRepository = new HttpOperadorRepository();
const tipoComprobanteRepository = new HttpTipoComprobanteRepository();
const conceptoRepository = new HttpConceptoRepository();
const monedaRepository = new HttpMonedaRepository();
const ivaRepository = new HttpIvaRepository();
const tipoImpuestoRepository = new HttpTipoImpuestoRepository();
const articuloRepository = new HttpArticuloRepository();


// Use Cases Exports

export const getDomiciliosUseCase = new GetDomiciliosUseCase(domicilioRepository);
export const createDomicilioUseCase = new CreateDomicilioUseCase(domicilioRepository);
export const updateDomicilioUseCase = new UpdateDomicilioUseCase(domicilioRepository);
export const deleteDomicilioUseCase = new DeleteDomicilioUseCase(domicilioRepository);
export const getDomicilioByIdUseCase = new GetDomicilioByIdUseCase(domicilioRepository);

export const getTelefonosUseCase = new GetTelefonosUseCase(telefonoRepository);
export const createTelefonoUseCase = new CreateTelefonoUseCase(telefonoRepository);
export const updateTelefonoUseCase = new UpdateTelefonoUseCase(telefonoRepository);
export const deleteTelefonoUseCase = new DeleteTelefonoUseCase(telefonoRepository);

export const getOperadoresUseCase = new GetOperadoresUseCase(operadorRepository);
export const createOperadorUseCase = new CreateOperadorUseCase(operadorRepository);
export const deleteOperadorUseCase = new DeleteOperadorUseCase(operadorRepository);

export const getTiposComprobanteUseCase = new GetTiposComprobanteUseCase(tipoComprobanteRepository);
export const getConceptosUseCase = new GetConceptosUseCase(conceptoRepository);
export const getMonedasUseCase = new GetMonedasUseCase(monedaRepository);
export const getIvasUseCase = new GetIvasUseCase(ivaRepository);
export const createIvaUseCase = new CreateIvaUseCase(ivaRepository);
export const updateIvaUseCase = new UpdateIvaUseCase(ivaRepository);
export const deleteIvaUseCase = new DeleteIvaUseCase(ivaRepository);
export const createMonedaUseCase = new CreateMonedaUseCase(monedaRepository);
export const updateMonedaUseCase = new UpdateMonedaUseCase(monedaRepository);
export const deleteMonedaUseCase = new DeleteMonedaUseCase(monedaRepository);

export const createConceptoUseCase = new CreateConceptoUseCase(conceptoRepository);
export const updateConceptoUseCase = new UpdateConceptoUseCase(conceptoRepository);
export const deleteConceptoUseCase = new DeleteConceptoUseCase(conceptoRepository);

export const createTipoComprobanteUseCase = new CreateTipoComprobanteUseCase(tipoComprobanteRepository);
export const updateTipoComprobanteUseCase = new UpdateTipoComprobanteUseCase(tipoComprobanteRepository);
export const deleteTipoComprobanteUseCase = new DeleteTipoComprobanteUseCase(tipoComprobanteRepository);

export const getTiposImpuestoUseCase = new GetTiposImpuestoUseCase(tipoImpuestoRepository);
export const createTipoImpuestoUseCase = new CreateTipoImpuestoUseCase(tipoImpuestoRepository);
export const updateTipoImpuestoUseCase = new UpdateTipoImpuestoUseCase(tipoImpuestoRepository);
export const deleteTipoImpuestoUseCase = new DeleteTipoImpuestoUseCase(tipoImpuestoRepository);

export const updateOperadorUseCase = new UpdateOperadorUseCase(operadorRepository);

const comprobanteFullRepository = new AxiosComprobanteFullRepository();
export const createComprobanteFullUseCase = new CreateComprobanteFullUseCase(comprobanteFullRepository);

export const getCondicionesTributariasUseCase = new GetCondicionesTributariasUseCase(condicionTributariaRepository);
export const createCondicionTributariaUseCase = new CreateCondicionTributariaUseCase(condicionTributariaRepository);
export const updateCondicionTributariaUseCase = new UpdateCondicionTributariaUseCase(condicionTributariaRepository);
export const deleteCondicionTributariaUseCase = new DeleteCondicionTributariaUseCase(condicionTributariaRepository);

export const getArticulosUseCase = new GetArticulosUseCase(articuloRepository);
export const createArticuloUseCase = new CreateArticuloUseCase(articuloRepository);
export const updateArticuloUseCase = new UpdateArticuloUseCase(articuloRepository);
export const deleteArticuloUseCase = new DeleteArticuloUseCase(articuloRepository);
