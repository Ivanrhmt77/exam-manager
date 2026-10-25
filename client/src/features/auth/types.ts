export type UserRole = "admin" | "lecturer" | "student";

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  nip: string | null;
  nrp: string | null;
  mustChangePassword: boolean;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  tokenType: string;
}

export interface AuthSession {
  tokens: AuthTokens;
  user: User;
  mustChangePassword: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface BackendUserDto {
  id: string;
  email: string;
  name: string;
  role: "admin" | "lecturer" | "student";
  nip: string | null;
  nrp: string | null;
  must_change_password: boolean;
}

export interface BackendTokenResponseDto {
  access_token: string;
  refresh_token: string;
  token_type: string;
  must_change_password: boolean;
  user: BackendUserDto;
}
