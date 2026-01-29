
import type { IMonedaRepository } from '../../../domain/repositories/IMonedaRepository';
import type { Moneda } from '../../../domain/entities/Moneda';

export class GetMonedasUseCase {
    constructor(private repository: IMonedaRepository) { }

    async execute(): Promise<Moneda[]> {
        return this.repository.getAll();
    }
}
