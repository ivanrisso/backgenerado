import type { ITipoDocRepository } from '../../../domain/repositories/ITipoDocRepository';
import type { TipoDoc } from '../../../domain/entities/TipoDoc';

export class CreateTipoDocUseCase {
    constructor(private readonly repository: ITipoDocRepository) { }

    async execute(entity: TipoDoc): Promise<void> {
        return this.repository.create(entity);
    }
}
