import type { TipoDom } from '../entities/TipoDom';

export interface ITipoDomRepository {
    getAll(): Promise<TipoDom[]>;
    getById(id: number): Promise<TipoDom | null>;
    create(entity: TipoDom): Promise<void>;
    update(entity: TipoDom): Promise<void>;
    delete(id: number): Promise<void>;
}
