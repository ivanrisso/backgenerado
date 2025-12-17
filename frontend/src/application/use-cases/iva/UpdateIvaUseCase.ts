
import type { IIvaRepository } from '../../../domain/repositories/IIvaRepository';
import type { Iva } from '../../../domain/entities/Iva';

export class UpdateIvaUseCase {
    constructor(private readonly repository: IIvaRepository) { }

    async execute(id: number, entity: Partial<Iva>): Promise<Iva> {
        return this.repository.update(id, entity);
    }
}
