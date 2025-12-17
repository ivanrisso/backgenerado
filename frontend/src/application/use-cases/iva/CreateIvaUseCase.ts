
import type { IIvaRepository } from '../../../domain/repositories/IIvaRepository';
import type { Iva } from '../../../domain/entities/Iva';

export class CreateIvaUseCase {
    constructor(private readonly repository: IIvaRepository) { }

    async execute(entity: Omit<Iva, 'id'>): Promise<Iva> {
        return this.repository.create(entity);
    }
}
