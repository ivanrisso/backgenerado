export class CUIT {
    constructor(public readonly value: string) {
        // Simple regex validation for AR CUIT (11 digits)
        if (!/^\d{11}$/.test(value)) {
            throw new Error(`Invalid CUIT: ${value}. Must be 11 digits.`);
        }
    }

    format(): string {
        // Format as XX-XXXXXXXX-X
        return `${this.value.slice(0, 2)}-${this.value.slice(2, 10)}-${this.value.slice(10)}`;
    }

    toString(): string {
        return this.value;
    }
}
