
import type { IMonedaRepository } from '../../../domain/repositories/IMonedaRepository';
import type { Moneda } from '../../../domain/entities/Moneda';

export class UpdateMonedaUseCase {
    constructor(private readonly repository: IMonedaRepository) { }

    async execute(id: number, entity: Partial<Moneda>): Promise<Moneda> {
        return this.repository.update(id, entity);
    }
}
