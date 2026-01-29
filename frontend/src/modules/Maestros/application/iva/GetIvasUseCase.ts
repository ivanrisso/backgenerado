
import type { IIvaRepository } from '../../../domain/repositories/IIvaRepository';
import type { Iva } from '../../../domain/entities/Iva';

export class GetIvasUseCase {
    constructor(private repository: IIvaRepository) { }

    async execute(): Promise<Iva[]> {
        return this.repository.getAll();
    }
}
