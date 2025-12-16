export abstract class ValueObject<T> {
    protected readonly _value: T;

    constructor(value: T) {
        this.validate(value);
        this._value = value;
    }

    get value(): T {
        return this._value;
    }

    protected abstract validate(value: T): void;

    equals(other: ValueObject<T>): boolean {
        return other.constructor.name === this.constructor.name && other.value === this._value;
    }
}
