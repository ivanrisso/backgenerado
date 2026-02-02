import type { AxiosAuthRepository } from '@infra/repositories/AxiosAuthRepository';

export class LoginUseCase {
    constructor(private readonly repository: AxiosAuthRepository) { }

    async execute(email: string, password: string): Promise<void> {
        return await this.repository.login(email, password);
    }
}
