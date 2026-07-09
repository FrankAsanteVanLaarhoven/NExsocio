"use client";

import { ModeBadge } from "@nexus/ui";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { BrandLogo } from "@/components/BrandLogo";
import { AppIcon, type AppIconName } from "@/components/icons/AppIcon";
import { useTranslation } from "@/i18n";
import { useAuthHydrated } from "@/hooks/useAuthHydrated";
import { useAuthStore } from "@/lib/auth-store";
import { APP_CONTAINER } from "@/lib/layout";
import { useSettingsStore } from "@/lib/settings-store";

const DOCK: { href: string; labelKey: string; icon: AppIconName }[] = [
  { href: "/feed", labelKey: "nav.feed", icon: "feed" },
  { href: "/twin", labelKey: "nav.twin", icon: "twin" },
  { href: "/studio", labelKey: "nav.studio", icon: "studio" },
  { href: "/live", labelKey: "nav.live", icon: "live" },
  { href: "/status", labelKey: "nav.status", icon: "status" },
  { href: "/calls", labelKey: "nav.calls", icon: "calls" },
  { href: "/teams", labelKey: "nav.teams", icon: "teams" },
  { href: "/contacts", labelKey: "nav.contacts", icon: "contacts" },
  { href: "/hub", labelKey: "nav.hub", icon: "hub" },
  { href: "/marketplace", labelKey: "nav.market", icon: "market" },
  { href: "/map", labelKey: "nav.map", icon: "map" },
  { href: "/find", labelKey: "nav.find", icon: "find" },
  { href: "/connections", labelKey: "nav.connect", icon: "connect" },
  { href: "/inbox", labelKey: "nav.inbox", icon: "inbox" },
  { href: "/settings", labelKey: "nav.settings", icon: "settings" },
];

export function EphemeralHeader() {
  const { t } = useTranslation();
  const pathname = usePathname();
  const hydrated = useAuthHydrated();
  const session = useAuthStore((s) => s.session);
  const viewContext = session?.viewContext ?? "personal";
  const setViewContext = useAuthStore((s) => s.setViewContext);
  const clearSession = useAuthStore((s) => s.clearSession);
  const ephemeralNav = useSettingsStore((s) => s.ephemeralNav);
  const voiceOn = useSettingsStore((s) => s.voiceControlEnabled);

  const [revealed, setRevealed] = useState(!ephemeralNav);
  const [nearTop, setNearTop] = useState(false);

  useEffect(() => {
    if (!ephemeralNav) {
      setRevealed(true);
      return;
    }
    const onScroll = () => setRevealed(window.scrollY > 48);
    const onMove = (e: MouseEvent) => setNearTop(e.clientY < 80);
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("mousemove", onMove, { passive: true });
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("mousemove", onMove);
    };
  }, [ephemeralNav]);

  const showNav = revealed || nearTop || !ephemeralNav;

  return (
    <header
      className={`sticky top-0 z-50 transition-all duration-500 ease-out ${
        showNav
          ? "border-b border-subtle backdrop-blur-xl shadow-[0_8px_32px_rgba(0,0,0,0.35)]"
          : "border-b border-transparent bg-transparent"
      }`}
      style={showNav ? { backgroundColor: "var(--color-header-bg)" } : undefined}
    >
      <div className={`${APP_CONTAINER} flex h-[4.5rem] items-center gap-5 lg:gap-8`}>
        <BrandLogo
          href="/"
          variant="header"
          size="lg"
          className={`shrink-0 transition-opacity duration-500 ${showNav ? "opacity-100" : "opacity-85"}`}
        />

        {hydrated && session && (
          <nav
            className={`min-w-0 flex-1 overflow-x-auto [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden transition-all duration-500 ${
              showNav ? "opacity-100 translate-y-0" : "opacity-0 translate-y-1 pointer-events-none"
            }`}
          >
            <div className="flex items-center gap-1.5 pr-2">
              {DOCK.map((item) => {
                const active = pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    title={t(item.labelKey)}
                    className={`flex shrink-0 items-center gap-1.5 rounded-lg px-3 py-2 text-[11px] font-medium uppercase tracking-wider transition-colors sm:text-xs ${
                      active
                        ? "bg-accent-muted text-accent shadow-[inset_0_0_0_1px_var(--color-accent-border)]"
                        : "text-faint hover:bg-surface-elevated hover:text-primary"
                    }`}
                  >
                    <AppIcon
                      name={item.icon}
                      size={16}
                      className={active ? "text-accent" : "text-faint"}
                    />
                    <span className="hidden lg:inline">{t(item.labelKey)}</span>
                  </Link>
                );
              })}
            </div>
          </nav>
        )}

        <div className="flex shrink-0 items-center gap-3">
          {voiceOn && (
            <span className="h-2.5 w-2.5 animate-pulse rounded-full bg-accent" title={t("nav.voiceActive")} />
          )}
          {hydrated && !session && (
            <>
              <Link href="/login" className="text-xs text-muted hover:text-accent">
                {t("nav.signIn")}
              </Link>
              <Link
                href="/register"
                className="rounded-lg border border-accent px-3 py-1.5 text-xs font-medium text-accent hover:bg-accent-muted"
              >
                {t("nav.register")}
              </Link>
            </>
          )}
          {hydrated && session && (
            <>
              <div className="hidden rounded-lg border border-default p-1 sm:flex">
                {(["personal", "professional"] as const).map((ctx) => (
                  <button
                    key={ctx}
                    type="button"
                    onClick={() => setViewContext(ctx)}
                    className={`rounded-md px-2.5 py-1 text-[10px] font-medium uppercase tracking-wider ${
                      viewContext === ctx
                        ? ctx === "professional"
                          ? "bg-[color-mix(in_srgb,var(--color-pro)_15%,transparent)] text-pro"
                          : "bg-accent-muted text-accent"
                        : "text-dim hover:text-primary"
                    }`}
                  >
                    {ctx === "personal" ? t("nav.persShort") : t("nav.profShort")}
                  </button>
                ))}
              </div>
              <ModeBadge mode={session.mode} />
              <button
                type="button"
                onClick={clearSession}
                className="text-[11px] font-medium text-dim hover:text-accent"
              >
                {t("nav.signOut")}
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}