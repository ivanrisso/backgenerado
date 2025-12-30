
import type { ITelefonoRepository } from '../../../domain/repositories/ITelefonoRepository';
import type { Telefono } from '../../../domain/entities/Telefono';

export class GetTelefonosUseCase {
    constructor(private repository: ITelefonoRepository) { }

    async execute(): Promise<Telefono[]> {
        return this.repository.getAll();
    }

    async executeByDomicilio(domicilioId: number): Promise<Telefono[]> {
        return this.repository.getByDomicilio(domicilioId);
    }
}
