import type { ILocalidadRepository } from '../../../domain/repositories/ILocalidadRepository';

export class DeleteLocalidadUseCase {
    constructor(private readonly repository: ILocalidadRepository) { }

    async execute(id: number): Promise<void> {
        return this.repository.delete(id);
    }
}
