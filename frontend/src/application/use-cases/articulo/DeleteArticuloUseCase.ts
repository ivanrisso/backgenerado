import type { ArticuloRepositoryInterface } from '../../../domain/repository/ArticuloRepositoryInterface';

export class DeleteArticuloUseCase {
    constructor(private repository: ArticuloRepositoryInterface) { }

    async execute(id: number): Promise<void> {
        return await this.repository.delete(id);
    }
}
