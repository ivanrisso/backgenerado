import type { AxiosAuthRepository } from '../../infrastructure/repositories/AxiosAuthRepository';
import type { Usuario } from '../../domain/entities/Usuario';

export class GetProfileUseCase {
    constructor(private readonly repository: AxiosAuthRepository) { }

    async execute(): Promise<Usuario> {
        return await this.repository.getProfile();
    }
}
