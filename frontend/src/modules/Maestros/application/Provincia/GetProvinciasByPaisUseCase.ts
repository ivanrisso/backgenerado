import type { IProvinciaRepository } from '../../../domain/repositories/IProvinciaRepository';
import type { Provincia } from '../../../domain/entities/Provincia';

export class GetProvinciasByPaisUseCase {
    constructor(private readonly repository: IProvinciaRepository) { }

    async execute(paisId: number): Promise<Provincia[]> {
        if (!paisId) throw new Error("Pais ID is required");
        return await this.repository.getAllByPais(paisId);
    }
}
