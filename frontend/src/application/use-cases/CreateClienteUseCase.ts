import type { IClienteRepository } from '@domain/repositories/IClienteRepository';
import type { Cliente } from '@domain/entities/Cliente';

export class CreateClienteUseCase {
    constructor(private readonly clienteRepository: IClienteRepository) { }

    async execute(cliente: Cliente): Promise<Cliente> {
        // Here we could add application validation logic if needed
        return this.clienteRepository.save(cliente);
    }
}
