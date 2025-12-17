
import type { IOperadorRepository } from '../../../domain/repositories/IOperadorRepository';
import type { Operador } from '../../../domain/entities/Operador';

export class UpdateOperadorUseCase {
    constructor(private readonly repository: IOperadorRepository) { }

    async execute(id: number, entity: Partial<Operador>): Promise<Operador> {
        return this.repository.update(id, entity);
    }
}
