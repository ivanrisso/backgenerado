
import type { ITelefonoRepository } from '../../../domain/repositories/ITelefonoRepository';

export class DeleteTelefonoUseCase {
    constructor(private repository: ITelefonoRepository) { }

    async execute(id: number): Promise<void> {
        return this.repository.delete(id);
    }
}
