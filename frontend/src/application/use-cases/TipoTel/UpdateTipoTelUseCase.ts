import type { ITipoTelRepository } from '../../../domain/repositories/ITipoTelRepository';
import type { TipoTel } from '../../../domain/entities/TipoTel';

export class UpdateTipoTelUseCase {
    constructor(private readonly repository: ITipoTelRepository) { }

    async execute(entity: TipoTel): Promise<void> {
        return this.repository.update(entity);
    }
}
