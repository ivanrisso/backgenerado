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



import { GetClientesUseCase } from '@app/use-cases/GetClientesUseCase';
import { CreateClienteUseCase } from '@app/use-cases/CreateClienteUseCase';
import { UpdateClienteUseCase } from '@app/use-cases/UpdateClienteUseCase';
import { GetClienteByIdUseCase } from '@app/use-cases/GetClienteByIdUseCase';
import { DeleteClienteUseCase } from '@app/use-cases/DeleteClienteUseCase';
import { GetAfipTaxComparisonUseCase } from '@app/use-cases/GetAfipTaxComparisonUseCase';
import { SyncAfipTaxesUseCase } from '@app/use-cases/SyncAfipTaxesUseCase';
import { GetCondicionesTributariasUseCase } from '@app/use-cases/condiciontributaria/GetCondicionesTributariasUseCase';



import { GetComprobantesUseCase } from '@app/use-cases/GetComprobantesUseCase';
import { CreateComprobanteUseCase } from '@app/use-cases/CreateComprobanteUseCase';

import { LoginUseCase } from '@app/use-cases/LoginUseCase';
import { LogoutUseCase } from '@app/use-cases/LogoutUseCase';
import { GetProfileUseCase } from '@app/use-cases/GetProfileUseCase';

// New UseCase Imports
import { GetTiposDocUseCase } from '@app/use-cases/TipoDoc/GetTiposDocUseCase';
import { GetTipoDocByIdUseCase } from '@app/use-cases/TipoDoc/GetTipoDocByIdUseCase';
import { CreateTipoDocUseCase } from '@app/use-cases/TipoDoc/CreateTipoDocUseCase';
import { UpdateTipoDocUseCase } from '@app/use-cases/TipoDoc/UpdateTipoDocUseCase';
import { DeleteTipoDocUseCase } from '@app/use-cases/TipoDoc/DeleteTipoDocUseCase';

import { GetPaisesUseCase } from '@app/use-cases/Pais/GetPaisesUseCase';
import { CreatePaisUseCase } from '@app/use-cases/Pais/CreatePaisUseCase';
import { UpdatePaisUseCase } from '@app/use-cases/Pais/UpdatePaisUseCase';
import { DeletePaisUseCase } from '@app/use-cases/Pais/DeletePaisUseCase';

import { GetProvinciasByPaisUseCase } from '@app/use-cases/Provincia/GetProvinciasByPaisUseCase';
import { CreateProvinciaUseCase } from '@app/use-cases/Provincia/CreateProvinciaUseCase';
import { UpdateProvinciaUseCase } from '@app/use-cases/Provincia/UpdateProvinciaUseCase';
import { DeleteProvinciaUseCase } from '@app/use-cases/Provincia/DeleteProvinciaUseCase';

import { GetLocalidadesByProvinciaUseCase } from '@app/use-cases/Localidad/GetLocalidadesByProvinciaUseCase';
import { CreateLocalidadUseCase } from '@app/use-cases/Localidad/CreateLocalidadUseCase';
import { UpdateLocalidadUseCase } from '@app/use-cases/Localidad/UpdateLocalidadUseCase';
import { DeleteLocalidadUseCase } from '@app/use-cases/Localidad/DeleteLocalidadUseCase';

import { GetTiposDomUseCase } from '@app/use-cases/TipoDom/GetTiposDomUseCase';
import { CreateTipoDomUseCase } from '@app/use-cases/TipoDom/CreateTipoDomUseCase';
import { UpdateTipoDomUseCase } from '@app/use-cases/TipoDom/UpdateTipoDomUseCase';
import { DeleteTipoDomUseCase } from '@app/use-cases/TipoDom/DeleteTipoDomUseCase';

import { GetTiposTelUseCase } from '@app/use-cases/TipoTel/GetTiposTelUseCase';
import { CreateTipoTelUseCase } from '@app/use-cases/TipoTel/CreateTipoTelUseCase';
import { UpdateTipoTelUseCase } from '@app/use-cases/TipoTel/UpdateTipoTelUseCase';
import { DeleteTipoTelUseCase } from '@app/use-cases/TipoTel/DeleteTipoTelUseCase';

import { GetLocalidadByIdUseCase } from '@app/use-cases/ubicacion/GetLocalidadByIdUseCase';
import { GetProvinciaByIdUseCase } from '@app/use-cases/ubicacion/GetProvinciaByIdUseCase';
// Auth & RBAC Imports
import { AxiosUsuarioRepository } from '@infra/repositories/AxiosUsuarioRepository';
import { AxiosRolRepository } from '@infra/repositories/AxiosRolRepository';
import { AxiosMenuItemRepository } from '@infra/repositories/AxiosMenuItemRepository';
import { AxiosAuthService } from '@infra/services/AxiosAuthService';

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

import { AuthUseCase } from '@app/usecases/auth/AuthUseCase';

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

import { GetArticulosUseCase } from '@app/use-cases/articulo/GetArticulosUseCase';
import { CreateArticuloUseCase } from '@app/use-cases/articulo/CreateArticuloUseCase';
import { UpdateArticuloUseCase } from '@app/use-cases/articulo/UpdateArticuloUseCase';
import { DeleteArticuloUseCase } from '@app/use-cases/articulo/DeleteArticuloUseCase';

import { GetDomiciliosUseCase } from '@app/use-cases/domicilio/GetDomiciliosUseCase';
import { CreateDomicilioUseCase } from '@app/use-cases/domicilio/CreateDomicilioUseCase';
import { UpdateDomicilioUseCase } from '@app/use-cases/domicilio/UpdateDomicilioUseCase';
import { DeleteDomicilioUseCase } from '@app/use-cases/domicilio/DeleteDomicilioUseCase';
import { GetDomicilioByIdUseCase } from '@app/use-cases/domicilio/GetDomicilioByIdUseCase';

import { GetTelefonosUseCase } from '@app/use-cases/telefono/GetTelefonosUseCase';
import { CreateTelefonoUseCase } from '@app/use-cases/telefono/CreateTelefonoUseCase';
import { UpdateTelefonoUseCase } from '@app/use-cases/telefono/UpdateTelefonoUseCase';
import { DeleteTelefonoUseCase } from '@app/use-cases/telefono/DeleteTelefonoUseCase';

import { GetOperadoresUseCase } from '@app/use-cases/operador/GetOperadoresUseCase';
import { CreateOperadorUseCase } from '@app/use-cases/operador/CreateOperadorUseCase';
import { DeleteOperadorUseCase } from '@app/use-cases/operador/DeleteOperadorUseCase';

import { GetTiposComprobanteUseCase } from '@app/use-cases/tipocomprobante/GetTiposComprobanteUseCase';
import { GetConceptosUseCase } from '@app/use-cases/concepto/GetConceptosUseCase';
import { GetMonedasUseCase } from '@app/use-cases/moneda/GetMonedasUseCase';
import { GetIvasUseCase } from '@app/use-cases/iva/GetIvasUseCase';

import { GetTiposImpuestoUseCase } from '@app/use-cases/tipoimpuesto/GetTiposImpuestoUseCase';
import { CreateTipoImpuestoUseCase } from '@app/use-cases/tipoimpuesto/CreateTipoImpuestoUseCase';
import { UpdateTipoImpuestoUseCase } from '@app/use-cases/tipoimpuesto/UpdateTipoImpuestoUseCase';
import { DeleteTipoImpuestoUseCase } from '@app/use-cases/tipoimpuesto/DeleteTipoImpuestoUseCase';
import { CreateIvaUseCase } from '@app/use-cases/iva/CreateIvaUseCase';
import { UpdateIvaUseCase } from '@app/use-cases/iva/UpdateIvaUseCase';
import { DeleteIvaUseCase } from '@app/use-cases/iva/DeleteIvaUseCase';


import { CreateMonedaUseCase } from '@app/use-cases/moneda/CreateMonedaUseCase';

import { UpdateMonedaUseCase } from '@app/use-cases/moneda/UpdateMonedaUseCase';
import { DeleteMonedaUseCase } from '@app/use-cases/moneda/DeleteMonedaUseCase';

import { CreateConceptoUseCase } from '@app/use-cases/concepto/CreateConceptoUseCase';
import { UpdateConceptoUseCase } from '@app/use-cases/concepto/UpdateConceptoUseCase';
import { DeleteConceptoUseCase } from '@app/use-cases/concepto/DeleteConceptoUseCase';

import { CreateTipoComprobanteUseCase } from '@app/use-cases/tipocomprobante/CreateTipoComprobanteUseCase';
import { UpdateTipoComprobanteUseCase } from '@app/use-cases/tipocomprobante/UpdateTipoComprobanteUseCase';
import { DeleteTipoComprobanteUseCase } from '@app/use-cases/tipocomprobante/DeleteTipoComprobanteUseCase';

import { UpdateOperadorUseCase } from '@app/use-cases/operador/UpdateOperadorUseCase';
import { AxiosComprobanteFullRepository } from '@infra/repositories/AxiosComprobanteFullRepository';
import { CreateComprobanteFullUseCase } from '@app/use-cases/comprobante/CreateComprobanteFullUseCase';

import { CreateCondicionTributariaUseCase } from '@app/use-cases/condiciontributaria/CreateCondicionTributariaUseCase';
import { UpdateCondicionTributariaUseCase } from '@app/use-cases/condiciontributaria/UpdateCondicionTributariaUseCase';
import { DeleteCondicionTributariaUseCase } from '@app/use-cases/condiciontributaria/DeleteCondicionTributariaUseCase';

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
export const authUseCase = new AuthUseCase(authService);

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

