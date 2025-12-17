
import { ValueObject } from './ValueObject';

interface PorcentajeProps {
    value: number;
}

export class Porcentaje extends ValueObject<PorcentajeProps> {
    private constructor(props: PorcentajeProps) {
        super(props);
    }

    public static create(value: number): Porcentaje {
        if (value < 0) {
            throw new Error("El porcentaje no puede ser negativo");
        }
        // Additional business rules (e.g., max 100?) can be added here
        return new Porcentaje({ value });
    }

    get value(): number {
        return this.props.value;
    }

    public toString(): string {
        return `${this.props.value}%`;
    }
}
