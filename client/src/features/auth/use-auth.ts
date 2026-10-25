"use client";

import { useCallback, useEffect, useState } from "react";
import { getSession, login as serviceLogin, logout as serviceLogout, verifySession as serviceVerify } from "./auth-service";
import { AuthSession, LoginCredentials } from "./types";

export type AuthStatus = "loading" | "authenticated" | "unauthenticated";

export function useAuth() {
  const [session, setSession] = useState<AuthSession | null>(() => getSession());
  const [status, setStatus] = useState<AuthStatus>(() => (getSession() ? "authenticated" : "loading"));

  useEffect(() => {
    let isMounted = true;

    serviceVerify()
      .then((verifiedSession) => {
        if (!isMounted) return;
        if (verifiedSession) {
          setSession(verifiedSession);
          setStatus("authenticated");
        } else {
          setSession(null);
          setStatus("unauthenticated");
        }
      })
      .catch(() => {
        if (!isMounted) return;
        setSession(null);
        setStatus("unauthenticated");
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const login = useCallback(async (credentials: LoginCredentials): Promise<AuthSession> => {
    const result = await serviceLogin(credentials);
    setSession(result);
    setStatus("authenticated");
    return result;
  }, []);

  const logout = useCallback(async (): Promise<void> => {
    try {
      await serviceLogout();
    } finally {
      setSession(null);
      setStatus("unauthenticated");
    }
  }, []);

  return {
    status,
    isLoading: status === "loading",
    isAuthenticated: status === "authenticated",
    user: session?.user ?? null,
    session,
    login,
    logout,
  };
}
