import type { ILocalidadRepository } from '../../../domain/repositories/ILocalidadRepository';
import type { Localidad } from '../../../domain/entities/Localidad';

export class GetLocalidadesByProvinciaUseCase {
    constructor(private readonly repository: ILocalidadRepository) { }

    async execute(provinciaId: number): Promise<Localidad[]> {
        if (!provinciaId) throw new Error("Provincia ID is required");
        return await this.repository.getAllByProvincia(provinciaId);
    }
}
