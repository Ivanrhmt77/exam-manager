"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/features/auth";

const Lecturer = () => {
  const router = useRouter();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    router.push("/login");
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-neutral-50 p-6">
      <div className="flex w-full max-w-md flex-col gap-4 rounded-xl border border-neutral-200 bg-white p-6 shadow-xs">
        <div className="flex flex-col gap-1">
          <h1 className="text-xl font-bold text-neutral-900">Dosen Dashboard</h1>
          <p className="text-sm text-neutral-500">
            Selamat datang, <span className="font-medium text-neutral-800">{user?.name}</span> ({user?.email})
          </p>
        </div>
        <div className="flex flex-col gap-2 rounded-lg bg-neutral-50 p-3 text-xs text-neutral-600">
          <div><span className="font-semibold">Role:</span> {user?.role}</div>
          {user?.nip && <div><span className="font-semibold">NIP:</span> {user?.nip}</div>}
          <div><span className="font-semibold">User ID:</span> {user?.id}</div>
        </div>
        <Button
          onClick={handleLogout}
          className="bg-primary-500 hover:bg-primary-700 cursor-pointer"
        >
          Logout
        </Button>
      </div>
    </div>
  );
};

export default Lecturer;
