import type { CondicionTributaria } from '@domain/entities/CondicionTributaria';
import type { ICondicionTributariaRepository } from '@domain/repositories/ICondicionTributariaRepository';

export class UpdateCondicionTributariaUseCase {
    constructor(private repository: ICondicionTributariaRepository) { }

    async execute(entity: CondicionTributaria): Promise<CondicionTributaria> {
        return this.repository.update(entity.id, entity);
    }
}
