
import type { IConceptoRepository } from '../../../domain/repositories/IConceptoRepository';
import type { Concepto } from '../../../domain/entities/Concepto';

export class GetConceptosUseCase {
    constructor(private repository: IConceptoRepository) { }

    async execute(): Promise<Concepto[]> {
        return this.repository.getAll();
    }
}
