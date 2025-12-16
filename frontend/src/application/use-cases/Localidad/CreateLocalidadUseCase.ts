import type { ILocalidadRepository } from '../../../domain/repositories/ILocalidadRepository';
import type { Localidad } from '../../../domain/entities/Localidad';

export class CreateLocalidadUseCase {
    constructor(private readonly repository: ILocalidadRepository) { }

    async execute(entity: Localidad): Promise<void> {
        return this.repository.create(entity);
    }
}
