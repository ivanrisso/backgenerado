import { Localidad } from '../../domain/entities/Localidad';

export class LocalidadMapper {
    static toDomain(dto: any): Localidad {
        return new Localidad(
            dto.id,
            dto.localidad_nombre, // snake_case
            dto.cod_postal,
            dto.provincia_id
        );
    }
}
