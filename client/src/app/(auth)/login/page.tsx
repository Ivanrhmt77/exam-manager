"use client";

import { Suspense } from "react";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import AppLogo from "@/shared/components/app-logo";
import Card from "@/shared/components/card";
import { ShieldCheck, BookOpen, ClipboardCheck, Loader2 } from "lucide-react";
import { useLoginForm } from "@/features/auth";

const LoginForm = () => {
  const {
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
  } = useLoginForm();

  return (
    <div className="flex min-h-screen w-full">
      <div className="bg-primary-50 border-primary-200 hidden w-[44%] max-w-140 flex-col justify-between border-r p-12 text-neutral-900 lg:flex">
        <div>
          <AppLogo />
        </div>
        <div className="flex flex-col gap-8">
          <div className="flex flex-col gap-3">
            <span className="type-headline-lg">
              Platform evaluasi akademik untuk perguruan tinggi.
            </span>
            <span className="text-sm text-neutral-500">
              Satu akun untuk seluruh alur ujian: dari penyusunan soal oleh
              dosen, pelaksanaan ujian online, hingga penilaian dan hasil.
            </span>
          </div>
          <div className="flex flex-col gap-3">
            <Card
              icon={ShieldCheck}
              title="Admin"
              description="Kelola dosen, mahasiswa, mata kuliah, dan kelas."
            />
            <Card
              icon={BookOpen}
              title="Dosen"
              description="Susun materi, bank soal, dan paket ujian dengan bantuan LLM."
            />
            <Card
              icon={ClipboardCheck}
              title="Mahasiswa"
              description="Kerjakan ujian online dan lihat hasil penilaian."
            />
          </div>
        </div>
        <div>
          <p className="text-xs text-neutral-500">© 2026 ExamManager </p>
        </div>
      </div>
      <div className="flex w-full flex-col items-center justify-center gap-8 bg-neutral-50 text-neutral-900">
        <div className="lg:hidden">
          <AppLogo />
        </div>
        <div className="flex w-100 flex-col gap-6 rounded-xl border border-neutral-200 bg-white p-8">
          <div className="flex flex-col gap-1.5">
            <span className="type-headline-md">Masuk ke ExamManager</span>
            <span className="text-sm text-neutral-500">
              Gunakan email dan password akun terdaftar Anda. Akun dibuat oleh
              Admin kampus.
            </span>
          </div>
          <div>
            <form onSubmit={handleSubmit} className="flex flex-col gap-5">
              {generalError && (
                <div
                  className="rounded-md border border-red-200 bg-red-50 p-3 text-xs text-red-600"
                  role="alert"
                >
                  {generalError}
                </div>
              )}

              <div className="flex flex-col gap-2">
                <Label htmlFor="email" className="text-xs">
                  Email
                </Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="nama@kampus.ac.id"
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={isSubmitting}
                  className="h-11 text-sm placeholder:text-neutral-400"
                  aria-invalid={Boolean(fieldErrors.email)}
                />
                {fieldErrors.email && (
                  <span className="text-xs text-red-600">
                    {fieldErrors.email}
                  </span>
                )}
              </div>

              <div className="flex flex-col gap-2">
                <Label htmlFor="password" className="text-xs">
                  Password
                </Label>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  placeholder="Masukkan password"
                  autoComplete="current-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={isSubmitting}
                  className="h-11 text-sm placeholder:text-neutral-400"
                  aria-invalid={Boolean(fieldErrors.password)}
                />
                {fieldErrors.password && (
                  <span className="text-xs text-red-600">
                    {fieldErrors.password}
                  </span>
                )}
              </div>

              <div className="flex justify-between">
                <div className="flex items-center gap-2">
                  <Checkbox
                    id="remember-me"
                    disabled
                    checked={rememberMe}
                    onCheckedChange={(checked) => setRememberMe(Boolean(checked))}
                    title="Fitur ini belum didukung oleh backend"
                    className="data-checked:bg-primary-500 data-checked:border-primary-500 cursor-not-allowed opacity-50"
                  />
                  <Label
                    htmlFor="remember-me"
                    className="cursor-not-allowed text-sm font-normal text-neutral-400"
                    title="Fitur ini belum didukung oleh backend"
                  >
                    Ingat saya
                  </Label>
                </div>
                <a href="" className="text-primary-500 text-sm">
                  Lupa password?
                </a>
              </div>

              <Button
                type="submit"
                disabled={isSubmitting}
                className="bg-primary-500 hover:bg-primary-700 w-full cursor-pointer p-2 text-sm font-medium disabled:cursor-not-allowed disabled:opacity-50"
              >
                {isSubmitting ? (
                  <span className="flex items-center justify-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Memproses...
                  </span>
                ) : (
                  "Masuk"
                )}
              </Button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

const LoginPage = () => {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen items-center justify-center">
          <Loader2 className="h-8 w-8 animate-spin text-primary-500" />
        </div>
      }
    >
      <LoginForm />
    </Suspense>
  );
};

export default LoginPage;
