import type { IClienteRepository } from '@domain/repositories/IClienteRepository';
import type { Cliente } from '@domain/entities/Cliente';

export class GetClienteByIdUseCase {
    constructor(private readonly clienteRepository: IClienteRepository) { }

    async execute(id: number): Promise<Cliente | null> {
        return this.clienteRepository.getById(id);
    }
}
