import type { ITipoDomRepository } from '../../../domain/repositories/ITipoDomRepository';

export class DeleteTipoDomUseCase {
    constructor(private readonly repository: ITipoDomRepository) { }

    async execute(id: number): Promise<void> {
        return this.repository.delete(id);
    }
}
