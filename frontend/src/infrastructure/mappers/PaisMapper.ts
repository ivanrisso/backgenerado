import { Pais } from '../../domain/entities/Pais';
import { CodigoPais } from '../../domain/value-objects/CodigoPais';

export class PaisMapper {
    static toDomain(dto: any): Pais {
        return new Pais(
            dto.id,
            dto.nombre,
            new CodigoPais(dto.codigo || '')
        );
    }
}
