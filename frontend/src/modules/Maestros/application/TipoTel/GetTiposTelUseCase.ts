import type { ITipoTelRepository } from '../../../domain/repositories/ITipoTelRepository';
import type { TipoTel } from '../../../domain/entities/TipoTel';

export class GetTiposTelUseCase {
    constructor(private readonly repository: ITipoTelRepository) { }

    async execute(): Promise<TipoTel[]> {
        return await this.repository.getAll();
    }
}
