
import type { ITelefonoRepository } from '../../../domain/repositories/ITelefonoRepository';
import type { Telefono } from '../../../domain/entities/Telefono';

export class UpdateTelefonoUseCase {
    constructor(private repository: ITelefonoRepository) { }

    async execute(id: number, telefono: Partial<Telefono>): Promise<Telefono> {
        return this.repository.update(id, telefono);
    }
}
