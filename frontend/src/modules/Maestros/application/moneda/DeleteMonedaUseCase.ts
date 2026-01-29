
import type { IMonedaRepository } from '../../../domain/repositories/IMonedaRepository';

export class DeleteMonedaUseCase {
    constructor(private readonly repository: IMonedaRepository) { }

    async execute(id: number): Promise<void> {
        return this.repository.delete(id);
    }
}
