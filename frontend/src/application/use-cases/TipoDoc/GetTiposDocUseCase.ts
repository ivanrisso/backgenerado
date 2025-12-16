import type { ITipoDocRepository } from '../../../domain/repositories/ITipoDocRepository';
import type { TipoDoc } from '../../../domain/entities/TipoDoc';

export class GetTiposDocUseCase {
    constructor(private readonly repository: ITipoDocRepository) { }

    async execute(): Promise<TipoDoc[]> {
        return await this.repository.getAll();
    }
}
