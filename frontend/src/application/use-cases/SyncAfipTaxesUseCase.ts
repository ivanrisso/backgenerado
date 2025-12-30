import type { IClienteRepository } from '../../domain/repositories/IClienteRepository';

export class SyncAfipTaxesUseCase {
    constructor(private readonly repository: IClienteRepository) { }

    async execute(id: number, afipIds: string[]): Promise<any> {
        return await this.repository.syncAfipTaxes(id, afipIds);
    }
}
