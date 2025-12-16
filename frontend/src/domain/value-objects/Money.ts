export class Money {
    constructor(public readonly amount: number, public readonly currency: string = 'ARS') { }

    static from(amount: number, currency: string = 'ARS'): Money {
        return new Money(amount, currency);
    }

    add(other: Money): Money {
        if (other.currency !== this.currency) {
            throw new Error(`Cannot add different currencies: ${this.currency} vs ${other.currency}`);
        }
        return new Money(this.amount + other.amount, this.currency);
    }

    format(): string {
        return new Intl.NumberFormat('es-AR', { style: 'currency', currency: this.currency }).format(this.amount);
    }
}
