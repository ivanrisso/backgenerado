import { LoginUseCase } from "./application/LoginUseCase";
import { AxiosAuthRepository } from "@infra/repositories/AxiosAuthRepository";

const authRepository = new AxiosAuthRepository();

export const loginUseCase = new LoginUseCase(authRepository);
