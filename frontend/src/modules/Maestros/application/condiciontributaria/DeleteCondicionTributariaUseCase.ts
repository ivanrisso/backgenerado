import type { ICondicionTributariaRepository } from '@domain/repositories/ICondicionTributariaRepository';

export class DeleteCondicionTributariaUseCase {
    constructor(private repository: ICondicionTributariaRepository) { }

    async execute(id: number): Promise<void> {
        return this.repository.delete(id);
    }
}
