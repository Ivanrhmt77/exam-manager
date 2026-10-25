"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { getApiErrorMessage } from "../../lib/api-client";
import { useAuth } from "./use-auth";
import { UserRole } from "./types";

interface FieldErrors {
  email?: string;
  password?: string;
}

export function getRoleDefaultPath(role: UserRole): string {
  switch (role) {
    case "admin":
      return "/admin";
    case "lecturer":
      return "/lecturer";
    case "student":
      return "/student";
    default:
      return "/login";
  }
}

export function isSafeRedirect(path: string | null): boolean {
  if (!path) return false;
  if (!path.startsWith("/")) return false;
  if (path.startsWith("//") || path.startsWith("/\\")) return false;
  if (path.includes(":")) return false;
  return true;
}

export function isPathAllowedForRole(path: string, role: UserRole): boolean {
  if (role === "admin" && (path.startsWith("/admin") || path === "/")) return true;
  if (role === "lecturer" && (path.startsWith("/lecturer") || path === "/")) return true;
  if (role === "student" && (path.startsWith("/student") || path === "/")) return true;
  return false;
}

export function useLoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [generalError, setGeneralError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validate = (): boolean => {
    const errors: FieldErrors = {};

    if (!email.trim()) {
      errors.email = "Email wajib diisi";
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email.trim())) {
        errors.email = "Format email tidak valid";
      }
    }

    if (!password) {
      errors.password = "Password wajib diisi";
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (isSubmitting) return;

    setGeneralError(null);

    if (!validate()) {
      return;
    }

    setIsSubmitting(true);

    try {
      const session = await login({
        email: email.trim(),
        password,
      });

      const redirectParam = searchParams.get("redirect");
      const defaultPath = getRoleDefaultPath(session.user.role);

      let targetPath = defaultPath;
      if (
        isSafeRedirect(redirectParam) &&
        isPathAllowedForRole(redirectParam!, session.user.role)
      ) {
        targetPath = redirectParam!;
      }

      router.push(targetPath);
      router.refresh();
    } catch (err: unknown) {
      const message = getApiErrorMessage(err);
      setGeneralError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return {
    email,
    setEmail,
    password,
    setPassword,
    rememberMe,
    setRememberMe,
    fieldErrors,
    generalError,
    isSubmitting,
    handleSubmit,
  };
}
