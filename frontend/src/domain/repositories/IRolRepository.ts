import { Rol } from '../entities/Rol';

export interface IRolRepository {
    getAll(): Promise<Rol[]>;
    getById(id: number): Promise<Rol | null>;
    create(rol: Rol): Promise<void>;
    update(rol: Rol): Promise<void>;
    delete(id: number): Promise<void>;
}
