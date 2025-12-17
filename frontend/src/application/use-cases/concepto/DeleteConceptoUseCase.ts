
import type { IConceptoRepository } from '../../../domain/repositories/IConceptoRepository';

export class DeleteConceptoUseCase {
    constructor(private readonly repository: IConceptoRepository) { }

    async execute(id: number): Promise<void> {
        return this.repository.delete(id);
    }
}
