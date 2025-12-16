import type { IClienteRepository } from '@domain/repositories/IClienteRepository';
import type { Cliente } from '@domain/entities/Cliente';

export class GetClientesUseCase {
    constructor(private readonly clienteRepository: IClienteRepository) { }

    async execute(): Promise<Cliente[]> {
        return this.clienteRepository.getAll();
    }
}
