import type { Domicilio } from '../../../domain/entities/Domicilio';
import type { IDomicilioRepository } from '../../../domain/repositories/IDomicilioRepository';

export class GetDomicilioByIdUseCase {
    constructor(private readonly repository: IDomicilioRepository) { }

    async execute(id: number): Promise<Domicilio | null> {
        return await this.repository.getById(id);
    }
}
