import { httpClient } from '../api/httpClient';
import type { IAuthService } from '../../application/usecases/auth/AuthUseCase';
import type { Usuario } from '../../domain/entities/Usuario';
import { UsuarioMapper } from '../mappers/UsuarioMapper';
import type { UsuarioDTO } from '../dtos/UsuarioDTO';

export class AxiosAuthService implements IAuthService {

    async login(email: string, password: string): Promise<{ token: string; user: Usuario }> {
        // Updated to match Backend UsuarioLogin schema (JSON)
        const { data } = await httpClient.post<{ msg: string }>('/auth/login', {
            usuario_email: email,
            usuario_password: password
        });

        // Backend sets cookies. We don't get a token in response body for JSON login based on auth_routes.py.
        // auth_routes.py returns { "msg": "Inicio de sesión exitoso" } and sets cookies.

        // We set the localStorage flag for the router.
        localStorage.setItem('isLoggedIn', 'true');

        // After login, fetch user me
        const user = await this.getCurrentUser();
        if (!user) throw new Error('Failed to fetch user after login');

        return { token: '', user }; // Token is in cookie
    }

    async logout(): Promise<void> {
        // Simple client side cookie removal or call backend
        await httpClient.post('/auth/logout');
    }

    async getCurrentUser(): Promise<Usuario | null> {
        try {
            const { data } = await httpClient.get<UsuarioDTO>('/auth/me');
            return UsuarioMapper.toDomain(data);
        } catch (e) {
            return null;
        }
    }
}
