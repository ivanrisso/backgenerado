
import type { IComprobanteFullRepository } from '../../domain/repositories/IComprobanteFullRepository';
import type { ComprobanteFull } from '../../domain/entities/ComprobanteFull';
import { httpClient } from '../api/httpClient';
import { ComprobanteFullMapper } from '../mappers/ComprobanteFullMapper';

export class AxiosComprobanteFullRepository implements IComprobanteFullRepository {
    private readonly resource = '/comprobantes/full/';

    async create(comprobante: ComprobanteFull): Promise<ComprobanteFull> {
        const payload = ComprobanteFullMapper.toApi(comprobante);
        const response = await httpClient.post(this.resource, payload);
        return ComprobanteFullMapper.toDomain(response.data);
    }
}
