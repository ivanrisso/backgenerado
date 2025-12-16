import type { IPaisRepository } from '../../../domain/repositories/IPaisRepository';
import type { Pais } from '../../../domain/entities/Pais';

export class UpdatePaisUseCase {
    constructor(private readonly repository: IPaisRepository) { }

    async execute(entity: Pais): Promise<void> {
        return this.repository.update(entity);
    }
}
