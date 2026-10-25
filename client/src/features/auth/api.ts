import { apiClient } from "../../lib/api-client";
import {
  AuthSession,
  BackendTokenResponseDto,
  LoginCredentials,
  User,
  UserRole,
} from "./types";

export function mapUserDto(dto: BackendTokenResponseDto["user"]): User {
  return {
    id: dto.id,
    email: dto.email,
    name: dto.name,
    role: dto.role as UserRole,
    nip: dto.nip,
    nrp: dto.nrp,
    mustChangePassword: dto.must_change_password,
  };
}

export function mapTokenResponseDto(dto: BackendTokenResponseDto): AuthSession {
  return {
    tokens: {
      accessToken: dto.access_token,
      refreshToken: dto.refresh_token,
      tokenType: dto.token_type || "bearer",
    },
    user: mapUserDto(dto.user),
    mustChangePassword: dto.must_change_password,
  };
}

export async function loginApi(credentials: LoginCredentials): Promise<AuthSession> {
  const response = await apiClient.post<BackendTokenResponseDto>(
    "/api/v1/auth/login",
    {
      email: credentials.email,
      password: credentials.password,
    }
  );
  return mapTokenResponseDto(response.data);
}

export async function logoutApi(
  accessToken: string,
  refreshToken: string
): Promise<void> {
  await apiClient.post(
    "/api/v1/auth/logout",
    { refresh_token: refreshToken },
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );
}

export async function refreshTokenApi(refreshToken: string): Promise<AuthSession> {
  const response = await apiClient.post<BackendTokenResponseDto>(
    "/api/v1/auth/refresh",
    {
      refresh_token: refreshToken,
    }
  );
  return mapTokenResponseDto(response.data);
}

export async function verifySessionApi(accessToken: string): Promise<boolean> {
  const response = await apiClient.get<{ detail: string }>("/api/v1/auth/test-auth", {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  return response.status === 200;
}
