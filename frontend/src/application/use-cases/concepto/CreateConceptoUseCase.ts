
import type { IConceptoRepository } from '../../../domain/repositories/IConceptoRepository';
import type { Concepto } from '../../../domain/entities/Concepto';

export class CreateConceptoUseCase {
    constructor(private readonly repository: IConceptoRepository) { }

    async execute(entity: Omit<Concepto, 'id'>): Promise<Concepto> {
        return this.repository.create(entity);
    }
}
