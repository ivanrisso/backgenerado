
import type { ITipoComprobanteRepository } from '../../../domain/repositories/ITipoComprobanteRepository';
import type { TipoComprobante } from '../../../domain/entities/TipoComprobante';

export class GetTiposComprobanteUseCase {
    constructor(private repository: ITipoComprobanteRepository) { }

    async execute(): Promise<TipoComprobante[]> {
        return this.repository.getAll();
    }
}
