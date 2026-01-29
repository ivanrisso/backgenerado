
import type { IIvaRepository } from '../../../domain/repositories/IIvaRepository';

export class DeleteIvaUseCase {
    constructor(private readonly repository: IIvaRepository) { }

    async execute(id: number): Promise<void> {
        return this.repository.delete(id);
    }
}
