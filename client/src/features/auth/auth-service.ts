import {
  loginApi,
  logoutApi,
  refreshTokenApi,
  verifySessionApi,
} from "./api";
import {
  clearSession,
  getAccessToken,
  getRefreshToken,
  getStoredSession,
  saveSession,
} from "./storage";
import { AuthSession, LoginCredentials } from "./types";

export function validateLoginInput(credentials: LoginCredentials): void {
  if (!credentials.email || !credentials.email.trim()) {
    throw new Error("Email wajib diisi");
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(credentials.email.trim())) {
    throw new Error("Format email tidak valid");
  }
  if (!credentials.password) {
    throw new Error("Password wajib diisi");
  }
}

export async function login(credentials: LoginCredentials): Promise<AuthSession> {
  validateLoginInput(credentials);
  const session = await loginApi({
    email: credentials.email.trim(),
    password: credentials.password,
  });
  saveSession(session);
  return session;
}

export async function logout(): Promise<void> {
  const accessToken = getAccessToken();
  const refreshToken = getRefreshToken();
  try {
    if (accessToken && refreshToken) {
      await logoutApi(accessToken, refreshToken);
    }
  } catch {
  } finally {
    clearSession();
  }
}

export async function verifySession(): Promise<AuthSession | null> {
  const storedSession = getStoredSession();
  if (!storedSession) {
    return null;
  }

  try {
    const isValid = await verifySessionApi(storedSession.tokens.accessToken);
    if (isValid) {
      return storedSession;
    }
  } catch {
    const refreshToken = storedSession.tokens.refreshToken;
    if (refreshToken) {
      try {
        const refreshed = await refreshTokenApi(refreshToken);
        saveSession(refreshed);
        return refreshed;
      } catch {
        clearSession();
        return null;
      }
    }
  }

  clearSession();
  return null;
}

export function getSession(): AuthSession | null {
  return getStoredSession();
}
