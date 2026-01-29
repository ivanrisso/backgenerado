import type { Articulo } from '../../../domain/entities/Articulo';
import type { ArticuloRepositoryInterface } from '../../../domain/repository/ArticuloRepositoryInterface';

export class CreateArticuloUseCase {
    constructor(private repository: ArticuloRepositoryInterface) { }

    async execute(articulo: Articulo): Promise<Articulo> {
        return await this.repository.create(articulo);
    }
}
