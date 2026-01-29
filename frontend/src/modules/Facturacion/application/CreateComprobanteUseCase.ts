import type { IComprobanteRepository } from '@domain/repositories/IComprobanteRepository';
import type { Comprobante } from '@domain/entities/Comprobante';

export class CreateComprobanteUseCase {
    constructor(private readonly comprobanteRepository: IComprobanteRepository) { }

    async execute(comprobante: Comprobante): Promise<Comprobante> {
        return this.comprobanteRepository.save(comprobante);
    }
}
