
import type { ITipoDocRepository } from '../../domain/repositories/ITipoDocRepository';
import type { TipoDoc } from '../../domain/entities/TipoDoc';
import { axiosClient } from '../api/axiosClient';

export class AxiosTipoDocRepository implements ITipoDocRepository {
    private readonly resource = '/tipodocs';

    async getAll(): Promise<TipoDoc[]> {
        const { data } = await axiosClient.get<any[]>(this.resource);
        return data.map(d => this.mapToEntity(d));
    }

    async getById(id: number): Promise<TipoDoc | null> {
        try {
            const { data } = await axiosClient.get<any>(`${this.resource}/${id}`);
            return this.mapToEntity(data);
        } catch (error: any) {
            if (error.response?.status === 404) return null;
            throw error;
        }
    }

    async create(entity: TipoDoc): Promise<void> {
        // Map domain to DTO if needed. backend expects snake_case probably.
        const dto = { tipo_doc_nombre: entity.nombre, codigo_arca: entity.codigoArca?.value, habilitado: entity.habilitado };
        await axiosClient.post(this.resource, dto);
    }

    async update(entity: TipoDoc): Promise<void> {
        const dto = { tipo_doc_nombre: entity.nombre, codigo_arca: entity.codigoArca?.value, habilitado: entity.habilitado };
        await axiosClient.patch(`${this.resource}/${entity.id}`, dto);
    }

    async delete(id: number): Promise<void> {
        await axiosClient.delete(`${this.resource}/${id}`);
    }

    private mapToEntity(d: any): TipoDoc {
        return {
            id: d.id,
            nombre: d.tipo_doc_nombre,
            habilitado: d.habilitado,
            codigoArca: d.codigo_arca ? { value: d.codigo_arca } : undefined
        } as unknown as TipoDoc;
    }
}
