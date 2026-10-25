import axios, { AxiosError } from "axios";

export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

export function getApiErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const err = error as AxiosError<{ detail?: string | Array<{ msg: string }> }>;
    const data = err.response?.data;
    if (data?.detail) {
      if (typeof data.detail === "string") {
        return data.detail;
      }
      if (Array.isArray(data.detail) && data.detail.length > 0) {
        return data.detail.map((item) => item.msg).join(", ");
      }
    }
    if (err.response?.status === 401) {
      return "Kredensial tidak valid atau sesi telah berakhir.";
    }
    if (err.response?.status === 403) {
      return "Anda tidak memiliki izin untuk mengakses resource ini.";
    }
    if (err.code === "ECONNABORTED" || err.message.includes("Network Error") || !err.response) {
      return "Gagal terhubung ke server. Periksa koneksi internet Anda.";
    }
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "Terjadi kesalahan yang tidak terduga.";
}
