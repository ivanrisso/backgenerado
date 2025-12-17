
import type { IDomicilioRepository } from '../../../domain/repositories/IDomicilioRepository';

export class DeleteDomicilioUseCase {
    constructor(private repository: IDomicilioRepository) { }

    async execute(id: number): Promise<void> {
        return this.repository.delete(id);
    }
}
