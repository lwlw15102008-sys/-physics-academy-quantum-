import AdminShell from "@/components/AdminShell";
import { authEnforced } from "@/lib/sections";

export default function ConsoleLayout({ children }: { children: React.ReactNode }) {
  return <AdminShell authEnforced={authEnforced()}>{children}</AdminShell>;
}
