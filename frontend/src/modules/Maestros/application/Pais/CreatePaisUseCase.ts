import type { IPaisRepository } from '../../../domain/repositories/IPaisRepository';
import type { Pais } from '../../../domain/entities/Pais';

export class CreatePaisUseCase {
    constructor(private readonly repository: IPaisRepository) { }

    async execute(entity: Pais): Promise<void> {
        return this.repository.create(entity);
    }
}
