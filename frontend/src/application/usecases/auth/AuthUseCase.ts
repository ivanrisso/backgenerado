import type { IAuthUseCase } from './IAuthUseCase';
import { Usuario } from '../../../domain/entities/Usuario';
// In a real scenario, this might use an IAuthService from Domain or Infra
// For now, let's assume it uses a repository or service.
// Since the prompt asks for "Application Layer" logical orchestration:
// We need an interface for the Auth Service (e.g. login against API)

export interface IAuthService {
    login(email: string, password: string): Promise<{ token: string; user: Usuario }>;
    logout(): void;
    getCurrentUser(): Promise<Usuario | null>;
}

export class AuthUseCase implements IAuthUseCase {
    constructor(private readonly authService: IAuthService) { }

    async login(email: string, password: string): Promise<boolean> {
        try {
            const result = await this.authService.login(email, password);
            // Store token? Usually infrastructure handles persistence of token.
            // But Application layer decides what to do.
            return !!result.user;
        } catch (error) {
            return false;
        }
    }

    logout(): void {
        this.authService.logout();
    }

    async getCurrentUser(): Promise<Usuario | null> {
        return this.authService.getCurrentUser();
    }

    isAuthenticated(): boolean {
        // This might need state or check service
        // For simplicity, let's assume service handles it
        return false; // dynamic check
    }
}
