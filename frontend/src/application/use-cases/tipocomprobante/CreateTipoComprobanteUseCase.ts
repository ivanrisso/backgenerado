
import type { ITipoComprobanteRepository } from '../../../domain/repositories/ITipoComprobanteRepository';
import type { TipoComprobante } from '../../../domain/entities/TipoComprobante';

export class CreateTipoComprobanteUseCase {
    constructor(private readonly repository: ITipoComprobanteRepository) { }

    async execute(entity: Omit<TipoComprobante, 'id'>): Promise<TipoComprobante> {
        return this.repository.create(entity);
    }
}
