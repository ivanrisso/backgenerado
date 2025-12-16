import { TipoTel } from '../../domain/entities/TipoTel';

export class TipoTelMapper {
    static toDomain(dto: any): TipoTel {
        return new TipoTel(
            dto.id,
            dto.nombre
        );
    }
}
