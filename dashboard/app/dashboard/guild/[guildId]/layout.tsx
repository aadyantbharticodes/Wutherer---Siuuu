"use client";

import { useParams } from "next/navigation";
import { Sidebar } from "@/components/dashboard/sidebar";

export default function GuildLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const params = useParams();
  const guildId = params.guildId as string;

  return (
    <div className="flex w-full min-w-0 flex-col lg:flex-row">
      <Sidebar guildId={guildId} />
      <main className="min-w-0 flex-1 px-4 py-6 sm:px-6 lg:px-8">
        <div className="mx-auto w-full max-w-7xl space-y-5">{children}</div>
      </main>
    </div>
  );
}
