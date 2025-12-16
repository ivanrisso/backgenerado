import { httpClient } from '../api/httpClient';
import type { Usuario } from '../../domain/entities/Usuario';

export class AxiosAuthRepository {
    private readonly resource = '/auth';

    async login(email: string, password: string): Promise<void> {
        await httpClient.post(`${this.resource}/login`, { usuario_email: email, usuario_password: password });
    }

    async logout(): Promise<void> {
        await httpClient.post(`${this.resource}/logout`);
    }

    async getProfile(): Promise<Usuario> {
        const response = await httpClient.get(`${this.resource}/me`);
        const data = response.data;
        return {
            id: data.id,
            email: data.usuario_email,
            nombre: data.nombre,
            apellido: data.apellido,
            roles: data.roles ? data.roles.map((r: any) => r.rol_nombre) : []
        };
    }
}
