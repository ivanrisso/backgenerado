
import type { IOperadorRepository } from '../../../domain/repositories/IOperadorRepository';
import type { Operador } from '../../../domain/entities/Operador';

export class GetOperadoresUseCase {
    constructor(private repository: IOperadorRepository) { }

    async execute(): Promise<Operador[]> {
        return this.repository.getAll();
    }
}
