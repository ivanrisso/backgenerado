import type { ILocalidadRepository } from '../../../domain/repositories/ILocalidadRepository';
import type { Localidad } from '../../../domain/entities/Localidad';

export class UpdateLocalidadUseCase {
    constructor(private readonly repository: ILocalidadRepository) { }

    async execute(entity: Localidad): Promise<void> {
        return this.repository.update(entity);
    }
}
