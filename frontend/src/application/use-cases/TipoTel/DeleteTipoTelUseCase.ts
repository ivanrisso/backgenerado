import type { ITipoTelRepository } from '../../../domain/repositories/ITipoTelRepository';

export class DeleteTipoTelUseCase {
    constructor(private readonly repository: ITipoTelRepository) { }

    async execute(id: number): Promise<void> {
        return this.repository.delete(id);
    }
}
