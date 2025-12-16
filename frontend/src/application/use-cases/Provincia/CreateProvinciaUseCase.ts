import type { IProvinciaRepository } from '../../../domain/repositories/IProvinciaRepository';
import type { Provincia } from '../../../domain/entities/Provincia';

export class CreateProvinciaUseCase {
    constructor(private readonly repository: IProvinciaRepository) { }

    async execute(entity: Provincia): Promise<void> {
        return this.repository.create(entity);
    }
}
