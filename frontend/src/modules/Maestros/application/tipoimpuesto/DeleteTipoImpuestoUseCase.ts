
import type { ITipoImpuestoRepository } from '@domain/repositories/ITipoImpuestoRepository';

export class DeleteTipoImpuestoUseCase {
    constructor(private readonly repository: ITipoImpuestoRepository) { }

    async execute(id: number): Promise<void> {
        return this.repository.delete(id);
    }
}
