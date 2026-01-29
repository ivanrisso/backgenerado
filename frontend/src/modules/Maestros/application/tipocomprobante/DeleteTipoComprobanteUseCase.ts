
import type { ITipoComprobanteRepository } from '../../../domain/repositories/ITipoComprobanteRepository';

export class DeleteTipoComprobanteUseCase {
    constructor(private readonly repository: ITipoComprobanteRepository) { }

    async execute(id: number): Promise<void> {
        return this.repository.delete(id);
    }
}
