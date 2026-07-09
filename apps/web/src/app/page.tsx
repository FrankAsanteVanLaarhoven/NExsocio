"use client";

import { useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Feed } from "@/components/Feed";
import { RegisterFlow } from "@/components/RegisterFlow";
import { useAuthStore } from "@/lib/auth-store";

export default function HomePage() {
  const session = useAuthStore((s) => s.session);
  const [registered, setRegistered] = useState(false);

  const showFeed = session !== null || registered;

  return (
    <AppShell>
      {showFeed ? <Feed /> : <RegisterFlow onComplete={() => setRegistered(true)} />}
    </AppShell>
  );
}