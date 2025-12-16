import type { IClienteRepository } from '../../domain/repositories/IClienteRepository';

export class DeleteClienteUseCase {
    constructor(private readonly repository: IClienteRepository) { }

    async execute(id: number): Promise<void> {
        return await this.repository.delete(id);
    }
}
