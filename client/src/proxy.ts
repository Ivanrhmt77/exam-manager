import { NextRequest, NextResponse } from "next/server";

const PROTECTED_ROUTES = ["/admin", "/lecturer", "/student"];
const AUTH_ROUTES = ["/login"];

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  const accessToken = request.cookies.get("auth_access_token")?.value;
  const refreshToken = request.cookies.get("auth_refresh_token")?.value;
  const hasTokens = Boolean(accessToken || refreshToken);

  const isProtectedRoute = PROTECTED_ROUTES.some(
    (route) => pathname === route || pathname.startsWith(`${route}/`)
  );
  const isAuthRoute = AUTH_ROUTES.some(
    (route) => pathname === route || pathname.startsWith(`${route}/`)
  );

  if (isProtectedRoute && !hasTokens) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  if (isAuthRoute && hasTokens) {
    const rawUser = request.cookies.get("auth_user")?.value;
    let targetPath = "/";

    if (rawUser) {
      try {
        const user = JSON.parse(decodeURIComponent(rawUser));
        if (user.role === "admin") targetPath = "/admin";
        else if (user.role === "lecturer") targetPath = "/lecturer";
        else if (user.role === "student") targetPath = "/student";
      } catch {
      }
    }

    return NextResponse.redirect(new URL(targetPath, request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico|.*\\.png$).*)"],
};
