import type { ITipoDomRepository } from '../../../domain/repositories/ITipoDomRepository';
import type { TipoDom } from '../../../domain/entities/TipoDom';

export class UpdateTipoDomUseCase {
    constructor(private readonly repository: ITipoDomRepository) { }

    async execute(entity: TipoDom): Promise<void> {
        return this.repository.update(entity);
    }
}
