
import type { ITipoComprobanteRepository } from '../../../domain/repositories/ITipoComprobanteRepository';
import type { TipoComprobante } from '../../../domain/entities/TipoComprobante';

export class UpdateTipoComprobanteUseCase {
    constructor(private readonly repository: ITipoComprobanteRepository) { }

    async execute(id: number, entity: Partial<TipoComprobante>): Promise<TipoComprobante> {
        return this.repository.update(id, entity);
    }
}
