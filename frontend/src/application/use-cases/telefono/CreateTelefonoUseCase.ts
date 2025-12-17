
import type { ITelefonoRepository } from '../../../domain/repositories/ITelefonoRepository';
import type { Telefono } from '../../../domain/entities/Telefono';

export class CreateTelefonoUseCase {
    constructor(private repository: ITelefonoRepository) { }

    async execute(telefono: Omit<Telefono, 'id'>): Promise<Telefono> {
        return this.repository.create(telefono);
    }
}
