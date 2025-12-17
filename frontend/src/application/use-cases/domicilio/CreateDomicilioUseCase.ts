
import type { IDomicilioRepository } from '../../../domain/repositories/IDomicilioRepository';
import type { Domicilio } from '../../../domain/entities/Domicilio';

export class CreateDomicilioUseCase {
    constructor(private repository: IDomicilioRepository) { }

    async execute(domicilio: Omit<Domicilio, 'id'>): Promise<Domicilio> {
        return this.repository.create(domicilio);
    }
}
