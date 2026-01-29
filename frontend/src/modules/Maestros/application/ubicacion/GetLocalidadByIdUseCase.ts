import type { ILocalidadRepository } from '../../../domain/repositories/ILocalidadRepository';
import type { Localidad } from '../../../domain/entities/Localidad';

export class GetLocalidadByIdUseCase {
    constructor(private repository: ILocalidadRepository) { }

    async execute(id: number): Promise<Localidad | null> {
        return await this.repository.getById(id);
    }
}
