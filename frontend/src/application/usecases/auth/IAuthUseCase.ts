import { Usuario } from '../../../domain/entities/Usuario';

export interface IAuthUseCase {
    login(email: string, password: string): Promise<boolean>;
    logout(): void;
    getCurrentUser(): Promise<Usuario | null>;
    isAuthenticated(): boolean;
}
