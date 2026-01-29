import type { ITipoDomRepository } from '../../../domain/repositories/ITipoDomRepository';
import type { TipoDom } from '../../../domain/entities/TipoDom';

export class GetTiposDomUseCase {
    constructor(private readonly repository: ITipoDomRepository) { }

    async execute(): Promise<TipoDom[]> {
        return await this.repository.getAll();
    }
}
