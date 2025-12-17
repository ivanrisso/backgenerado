
import type { IDomicilioRepository } from '../../../domain/repositories/IDomicilioRepository';
import type { Domicilio } from '../../../domain/entities/Domicilio';

export class GetDomiciliosUseCase {
    constructor(private repository: IDomicilioRepository) { }

    async execute(): Promise<Domicilio[]> {
        return this.repository.getAll();
    }
}
