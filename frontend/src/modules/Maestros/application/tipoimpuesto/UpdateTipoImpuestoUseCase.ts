
import type { ITipoImpuestoRepository } from '../../../domain/repositories/ITipoImpuestoRepository';
import type { TipoImpuesto } from '../../../domain/entities/TipoImpuesto';

export class UpdateTipoImpuestoUseCase {
    constructor(private repository: ITipoImpuestoRepository) { }

    async execute(id: number, entity: Partial<TipoImpuesto>): Promise<TipoImpuesto> {
        return this.repository.update(id, entity);
    }
}
