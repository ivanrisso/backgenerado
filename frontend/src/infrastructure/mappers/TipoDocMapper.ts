import { TipoDoc } from '../../domain/entities/TipoDoc';
import { CodigoArca } from '../../domain/value-objects/CodigoArca';

export class TipoDocMapper {
    static toDomain(dto: any): TipoDoc {
        return new TipoDoc(
            dto.id,
            dto.tipo_doc_nombre, // Mapping snake_case from DB
            dto.habilitado,
            new CodigoArca(dto.codigo_arca || '')
        );
    }
}
