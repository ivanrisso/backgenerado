import { ValueObject } from './ValueObject';

export class CodigoPais extends ValueObject<string> {
    protected validate(value: string): void {
        if (!value) {
            return; // Allow empty
        }
        // Relaxing rule: Allow 2 or 3 chars (e.g. AR or ARG)
        if (value.length < 2 || value.length > 3) {
            throw new Error(`El código de país '${value}' debe tener 2 o 3 caracteres`);
        }
    }
}
