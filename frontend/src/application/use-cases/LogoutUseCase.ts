import type { AxiosAuthRepository } from '../../infrastructure/repositories/AxiosAuthRepository';

export class LogoutUseCase {
    constructor(private readonly repository: AxiosAuthRepository) { }

    async execute(): Promise<void> {
        return await this.repository.logout();
    }
}
