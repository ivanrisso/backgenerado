
import type { IMonedaRepository } from '../../../domain/repositories/IMonedaRepository';
import type { Moneda } from '../../../domain/entities/Moneda';

export class CreateMonedaUseCase {
    constructor(private readonly repository: IMonedaRepository) { }

    async execute(entity: Omit<Moneda, 'id'>): Promise<Moneda> {
        return this.repository.create(entity);
    }
}
