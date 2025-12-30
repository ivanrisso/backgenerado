import type { Articulo } from '../../../domain/entities/Articulo';
import type { ArticuloRepositoryInterface } from '../../../domain/repository/ArticuloRepositoryInterface';

export class GetArticulosUseCase {
    constructor(private repository: ArticuloRepositoryInterface) { }

    async execute(): Promise<Articulo[]> {
        return await this.repository.getAll();
    }
}
