import { ValueObject } from './ValueObject';

export class CodigoArca extends ValueObject<string> {
    protected validate(value: string): void {
        // Allow empty string (some docs don't have ARCA code)
        if (!value) {
            return;
        }
        // Example rule: Max length 3 based on DB schema
        if (value.length > 3) {
            throw new Error(`El código ARCA '${value}' excede la longitud máxima de 3 caracteres`);
        }
    }
}
