import type { ITipoDocRepository } from '../../../domain/repositories/ITipoDocRepository';

export class DeleteTipoDocUseCase {
    constructor(private readonly repository: ITipoDocRepository) { }

    async execute(id: number): Promise<void> {
        return this.repository.delete(id);
    }
}
