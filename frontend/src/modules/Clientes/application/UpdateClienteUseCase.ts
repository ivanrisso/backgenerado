import type { IClienteRepository } from '@domain/repositories/IClienteRepository';
import type { Cliente } from '@domain/entities/Cliente';

export class UpdateClienteUseCase {
    constructor(private readonly clienteRepository: IClienteRepository) { }

    async execute(cliente: Cliente): Promise<Cliente> {
        return this.clienteRepository.update(cliente);
    }
}
