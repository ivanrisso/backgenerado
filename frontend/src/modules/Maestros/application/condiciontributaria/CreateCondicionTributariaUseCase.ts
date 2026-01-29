import type { CondicionTributaria } from '@domain/entities/CondicionTributaria';
import type { ICondicionTributariaRepository } from '@domain/repositories/ICondicionTributariaRepository';

export class CreateCondicionTributariaUseCase {
    constructor(private repository: ICondicionTributariaRepository) { }

    async execute(data: Omit<CondicionTributaria, 'id'>): Promise<CondicionTributaria> {
        return this.repository.create(data);
    }
}
