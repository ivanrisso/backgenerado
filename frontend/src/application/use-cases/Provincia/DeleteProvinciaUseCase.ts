import type { IProvinciaRepository } from '../../../domain/repositories/IProvinciaRepository';

export class DeleteProvinciaUseCase {
    constructor(private readonly repository: IProvinciaRepository) { }

    async execute(id: number): Promise<void> {
        return this.repository.delete(id);
    }
}
