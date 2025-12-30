import type { IProvinciaRepository } from '../../../domain/repositories/IProvinciaRepository';
import type { Provincia } from '../../../domain/entities/Provincia';

export class GetProvinciaByIdUseCase {
    constructor(private repository: IProvinciaRepository) { }

    async execute(id: number): Promise<Provincia | null> {
        return await this.repository.getById(id);
    }
}
