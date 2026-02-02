import type { IComprobanteFullRepository } from '@domain/repositories/IComprobanteFullRepository';
import type { ComprobanteFull } from '@domain/entities/ComprobanteFull';

export class CreateComprobanteFullUseCase {
    constructor(private readonly repository: IComprobanteFullRepository) { }

    async execute(comprobante: ComprobanteFull): Promise<ComprobanteFull> {
        return this.repository.create(comprobante);
    }
}
