
import type { ITipoImpuestoRepository } from '../../../domain/repositories/ITipoImpuestoRepository';
import type { TipoImpuesto } from '../../../domain/entities/TipoImpuesto';

export class GetTiposImpuestoUseCase {
    constructor(private repository: ITipoImpuestoRepository) { }

    async execute(): Promise<TipoImpuesto[]> {
        return this.repository.getAll();
    }
}
