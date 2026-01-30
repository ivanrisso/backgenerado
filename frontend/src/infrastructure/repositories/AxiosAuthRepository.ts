import { httpClient } from '../api/httpClient';
import type { Usuario } from '../../domain/entities/Usuario';
import { UsuarioMapper } from '../mappers/UsuarioMapper';
import type { UsuarioDTO } from '../dtos/UsuarioDTO';

export class AxiosAuthRepository {
    private readonly resource = '/auth';

    async login(email: string, password: string): Promise<void> {
        await httpClient.post(`${this.resource}/login`, { usuario_email: email, usuario_password: password });
        localStorage.setItem('isLoggedIn', 'true');

        // Validate session immediately to ensure cookie is set
        await this.getMe();
    }

    async logout(): Promise<void> {
        try {
            await httpClient.post(`${this.resource}/logout`);
        } finally {
            localStorage.removeItem('isLoggedIn');
        }
    }

    async getMe(): Promise<Usuario> {
        const response = await httpClient.get<UsuarioDTO>(`${this.resource}/me`);
        return UsuarioMapper.toDomain(response.data);
    }
}
