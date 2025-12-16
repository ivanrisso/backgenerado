export class Email {
    private readonly value: string;

    constructor(value: string) {
        if (!this.validate(value)) {
            throw new Error(`Invalid email format: ${value}`);
        }
        this.value = value;
    }

    private validate(email: string): boolean {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    getValue(): string {
        return this.value;
    }

    equals(other: Email): boolean {
        return this.value === other.value;
    }
}
