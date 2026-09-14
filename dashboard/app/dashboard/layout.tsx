import { DashboardHeader } from "@/components/dashboard/dashboard-header";

export default function DashboardRootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />
      <div className="min-h-[calc(100vh-4rem)]">{children}</div>
    </div>
  );
}

