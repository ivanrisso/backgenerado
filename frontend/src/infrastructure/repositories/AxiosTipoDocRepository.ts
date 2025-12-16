import type { TipoDoc } from '../../domain/entities/TipoDoc';
import { httpClient } from '../api/httpClient';

export class AxiosTipoDocRepository {
    private readonly resource = '/tipodocs';

    async getAll(): Promise<TipoDoc[]> {
        const { data } = await httpClient.get<any[]>(this.resource);
        return data.map(d => ({
            id: d.id,
            nombre: d.tipo_doc_nombre,
            habilitado: d.habilitado,
            codigoArca: { value: d.codigo_arca } // Mapping to match Entity structure if needed, or simple object
        }) as unknown as TipoDoc);
    }
}
