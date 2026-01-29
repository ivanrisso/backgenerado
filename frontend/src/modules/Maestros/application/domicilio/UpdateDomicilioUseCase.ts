
import type { IDomicilioRepository } from '../../../domain/repositories/IDomicilioRepository';
import type { Domicilio } from '../../../domain/entities/Domicilio';

export class UpdateDomicilioUseCase {
    constructor(private repository: IDomicilioRepository) { }

    async execute(id: number, domicilio: Partial<Domicilio>): Promise<Domicilio> {
        return this.repository.update(id, domicilio);
    }
}
