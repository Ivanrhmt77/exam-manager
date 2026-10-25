import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import AppLogo from "@/shared/components/app-logo";
import Card from "@/shared/components/card";
import { ShieldCheck, BookOpen, ClipboardCheck } from "lucide-react";

const login = () => {
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
            <form className="flex flex-col gap-5">
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
                  className="h-11 text-sm placeholder:text-neutral-400"
                />
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
                  className="h-11 text-sm placeholder:text-neutral-400"
                />
              </div>

              <div className="flex justify-between">
                <div className="flex items-center gap-2">
                  <Checkbox
                    id="remember-me"
                    className="data-checked:bg-primary-500 data-checked:border-primary-500 cursor-pointer"
                  />
                  <Label
                    htmlFor="remember-me"
                    className="cursor-pointer text-sm font-normal text-neutral-600"
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
                className="bg-primary-500 hover:bg-primary-700 w-full cursor-pointer p-2 text-sm font-medium"
              >
                Masuk
              </Button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default login;
