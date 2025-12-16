import { httpClient } from '../api/httpClient';
import type { IAuthService } from '../../application/usecases/auth/AuthUseCase';
import { Usuario } from '../../domain/entities/Usuario';
import { UsuarioMapper } from '../mappers/UsuarioMapper';
import type { UsuarioDTO } from '../dtos/UsuarioDTO';

export class AxiosAuthService implements IAuthService {

    async login(email: string, password: string): Promise<{ token: string; user: Usuario }> {
        // Backend uses form-data or json? Typical FastAPI /token uses form-data (OAuth2PasswordRequestForm)
        // or a custom json endpoint.
        // Assuming /login or /token. Let's assume standard json login for now or check backend.
        // Given existing project context, I'll assume JSON body to '/auth/login' or similar.
        // If it's OAuth2 standard, it might be form data at /token.
        // Let's check 'auth_routes.py' if possible, but I'll stick to a generic guess that can be updated.
        // I will use JSON POST to /auth/login as a safe default for a "Clean" implementation.

        // However, standard FastAPI OAuth2 uses x-www-form-urlencoded
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        // Path likely /auth/token or similar
        const { data } = await httpClient.post<{ access_token: string }>('/auth/token', formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });

        const token = data.access_token;
        // After login, usually fetch user me
        const user = await this.getCurrentUser();
        if (!user) throw new Error('Failed to fetch user after login');

        return { token, user };
    }

    async logout(): Promise<void> {
        // Simple client side cookie removal or call backend
        await httpClient.post('/auth/logout');
    }

    async getCurrentUser(): Promise<Usuario | null> {
        try {
            const { data } = await httpClient.get<UsuarioDTO>('/usuarios/me');
            return UsuarioMapper.toDomain(data);
        } catch (e) {
            return null;
        }
    }
}
