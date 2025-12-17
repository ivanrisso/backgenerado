
import type { ITelefonoRepository } from '../../../domain/repositories/ITelefonoRepository';
import type { Telefono } from '../../../domain/entities/Telefono';

export class GetTelefonosUseCase {
    constructor(private repository: ITelefonoRepository) { }

    async execute(): Promise<Telefono[]> {
        return this.repository.getAll();
    }
}
