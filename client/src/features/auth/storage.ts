import { AuthSession, User } from "./types";

const ACCESS_TOKEN_KEY = "auth_access_token";
const REFRESH_TOKEN_KEY = "auth_refresh_token";
const USER_KEY = "auth_user";

function isBrowser(): boolean {
  return typeof window !== "undefined" && typeof document !== "undefined";
}

function getCookie(name: string): string | null {
  if (!isBrowser()) return null;
  const match = document.cookie.match(new RegExp(`(^|;\\s*)(${name})=([^;]*)`));
  return match ? decodeURIComponent(match[3]) : null;
}

function setCookie(name: string, value: string, days: number = 7): void {
  if (!isBrowser()) return;
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  const isHttps = window.location.protocol === "https:";
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax${isHttps ? "; Secure" : ""}`;
}

function deleteCookie(name: string): void {
  if (!isBrowser()) return;
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; SameSite=Lax`;
}

export function getAccessToken(): string | null {
  return getCookie(ACCESS_TOKEN_KEY);
}

export function getRefreshToken(): string | null {
  return getCookie(REFRESH_TOKEN_KEY);
}

export function getStoredUser(): User | null {
  const raw = getCookie(USER_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as User;
  } catch {
    return null;
  }
}

export function getStoredSession(): AuthSession | null {
  const accessToken = getAccessToken();
  const refreshToken = getRefreshToken();
  const user = getStoredUser();

  if (!accessToken || !refreshToken || !user) {
    return null;
  }

  return {
    tokens: {
      accessToken,
      refreshToken,
      tokenType: "bearer",
    },
    user,
    mustChangePassword: user.mustChangePassword ?? false,
  };
}

export function saveSession(session: AuthSession): void {
  setCookie(ACCESS_TOKEN_KEY, session.tokens.accessToken, 1);
  setCookie(REFRESH_TOKEN_KEY, session.tokens.refreshToken, 7);
  setCookie(USER_KEY, JSON.stringify(session.user), 7);
}

export function clearSession(): void {
  deleteCookie(ACCESS_TOKEN_KEY);
  deleteCookie(REFRESH_TOKEN_KEY);
  deleteCookie(USER_KEY);
}
