
import type { IConceptoRepository } from '../../../domain/repositories/IConceptoRepository';
import type { Concepto } from '../../../domain/entities/Concepto';

export class UpdateConceptoUseCase {
    constructor(private readonly repository: IConceptoRepository) { }

    async execute(id: number, entity: Partial<Concepto>): Promise<Concepto> {
        return this.repository.update(id, entity);
    }
}
