import { Provincia } from '../../domain/entities/Provincia';

export class ProvinciaMapper {
    static toDomain(dto: any): Provincia {
        return new Provincia(
            dto.id,
            dto.provincia_nombre, // snake_case
            dto.pais_id
        );
    }
}
