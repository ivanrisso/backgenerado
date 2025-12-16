import type { IPaisRepository } from '../../../domain/repositories/IPaisRepository';
import type { Pais } from '../../../domain/entities/Pais';

export class GetPaisesUseCase {
    constructor(private readonly repository: IPaisRepository) { }

    async execute(): Promise<Pais[]> {
        return await this.repository.getAll();
    }
}
