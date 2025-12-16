import { TipoDom } from '../../domain/entities/TipoDom';

export class TipoDomMapper {
    static toDomain(dto: any): TipoDom {
        return new TipoDom(
            dto.id,
            dto.nombre
        );
    }
}
