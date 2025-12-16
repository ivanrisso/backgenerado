import type { Iva } from '../../domain/entities/Iva';
import { httpClient } from '../api/httpClient';

export class AxiosIvaRepository {
    private readonly resource = '/ivas';

    async getAll(): Promise<Iva[]> {
        const { data } = await httpClient.get<Iva[]>(this.resource);
        return data; // Using direct mapping as interface matches response closely or exactly
    }
}
