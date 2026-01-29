
import type { IOperadorRepository } from '../../../domain/repositories/IOperadorRepository';

export class DeleteOperadorUseCase {
    constructor(private repository: IOperadorRepository) { }

    async execute(id: number): Promise<void> {
        return this.repository.delete(id);
    }
}
