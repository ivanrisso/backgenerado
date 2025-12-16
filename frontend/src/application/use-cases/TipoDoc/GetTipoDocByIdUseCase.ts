import type { ITipoDocRepository } from '../../../domain/repositories/ITipoDocRepository';
import type { TipoDoc } from '../../../domain/entities/TipoDoc';

export class GetTipoDocByIdUseCase {
    constructor(private readonly repository: ITipoDocRepository) { }

    async execute(id: number): Promise<TipoDoc | null> {
        return await this.repository.getById(id);
    }
}
