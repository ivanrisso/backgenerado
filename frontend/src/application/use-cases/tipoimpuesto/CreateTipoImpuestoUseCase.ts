
import type { ITipoImpuestoRepository } from '../../../domain/repositories/ITipoImpuestoRepository';
import type { TipoImpuesto } from '../../../domain/entities/TipoImpuesto';

export class CreateTipoImpuestoUseCase {
    constructor(private repository: ITipoImpuestoRepository) { }

    async execute(entity: Omit<TipoImpuesto, 'id'>): Promise<TipoImpuesto> {
        return this.repository.create(entity);
    }
}
