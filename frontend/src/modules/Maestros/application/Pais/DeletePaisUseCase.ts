import type { IPaisRepository } from '../../../domain/repositories/IPaisRepository';

export class DeletePaisUseCase {
    constructor(private readonly repository: IPaisRepository) { }

    async execute(id: number): Promise<void> {
        return this.repository.delete(id);
    }
}
