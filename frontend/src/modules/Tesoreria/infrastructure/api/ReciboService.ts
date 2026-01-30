import { httpClient } from '../../../../shared/http/client';
import type { ReciboCreate, ReciboResponse } from '../../domain/models/Recibo';

export class ReciboService {
    private static readonly BASE_PATH = '/recibos';

    static async create(data: ReciboCreate): Promise<ReciboResponse> {
        const response = await httpClient.post<ReciboResponse>(this.BASE_PATH, data);
        return response.data;
    }
}
