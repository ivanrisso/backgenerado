import type { IClienteRepository } from '../../domain/repositories/IClienteRepository';

export class GetAfipTaxComparisonUseCase {
    constructor(private readonly repository: IClienteRepository) { }

    async execute(id: number): Promise<any> {
        return await this.repository.getAfipTaxComparison(id);
    }
}
