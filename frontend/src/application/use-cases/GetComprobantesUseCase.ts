import type { IComprobanteRepository } from '@domain/repositories/IComprobanteRepository';
import type { Comprobante } from '@domain/entities/Comprobante';

export class GetComprobantesUseCase {
    constructor(private readonly comprobanteRepository: IComprobanteRepository) { }

    async execute(): Promise<Comprobante[]> {
        return this.comprobanteRepository.getAll();
    }
}
