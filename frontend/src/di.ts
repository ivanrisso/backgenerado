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

import { GetClientesUseCase } from '@app/use-cases/GetClientesUseCase';
import { CreateClienteUseCase } from '@app/use-cases/CreateClienteUseCase';
import { UpdateClienteUseCase } from '@app/use-cases/UpdateClienteUseCase';
import { GetClienteByIdUseCase } from '@app/use-cases/GetClienteByIdUseCase';
import { DeleteClienteUseCase } from '@app/use-cases/DeleteClienteUseCase';

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

// Use Cases
export const getClientesUseCase = new GetClientesUseCase(clienteRepository);
export const createClienteUseCase = new CreateClienteUseCase(clienteRepository);
export const updateClienteUseCase = new UpdateClienteUseCase(clienteRepository);
export const getClienteByIdUseCase = new GetClienteByIdUseCase(clienteRepository);
export const deleteClienteUseCase = new DeleteClienteUseCase(clienteRepository);

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
