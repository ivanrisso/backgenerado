import type { Articulo } from '../../../domain/entities/Articulo';
import type { ArticuloRepositoryInterface } from '../../../domain/repository/ArticuloRepositoryInterface';

export class UpdateArticuloUseCase {
    constructor(private repository: ArticuloRepositoryInterface) { }

    async execute(id: number, articulo: Articulo): Promise<Articulo> {
        return await this.repository.update(id, articulo);
    }
}
