import type { CondicionTributaria } from '@domain/entities/CondicionTributaria';
import type { ICondicionTributariaRepository } from '@domain/repositories/ICondicionTributariaRepository';

export class GetCondicionesTributariasUseCase {
    constructor(private readonly repository: ICondicionTributariaRepository) { }

    async execute(): Promise<CondicionTributaria[]> {
        return await this.repository.getAll();
    }
}
