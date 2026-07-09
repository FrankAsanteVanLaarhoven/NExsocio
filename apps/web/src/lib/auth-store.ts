"use client";

import type { AuthSession, UserMode, ViewContext } from "@nexus/types";
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface AuthState {
  session: AuthSession | null;
  feedType: "global" | "connections";
  setSession: (session: AuthSession) => void;
  updateMode: (mode: UserMode, accessToken: string) => void;
  updateDisplayName: (displayName: string) => void;
  setViewContext: (context: ViewContext) => void;
  setFeedType: (feedType: "global" | "connections") => void;
  clearSession: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      session: null,
      feedType: "global",
      setSession: (session) =>
        set({
          session: {
            ...session,
            viewContext: session.viewContext ?? "personal",
          },
        }),
      updateMode: (mode, accessToken) =>
        set((state) =>
          state.session ? { session: { ...state.session, mode, accessToken } } : state
        ),
      updateDisplayName: (displayName) =>
        set((state) =>
          state.session ? { session: { ...state.session, displayName } } : state
        ),
      setViewContext: (viewContext) =>
        set((state) => (state.session ? { session: { ...state.session, viewContext } } : state)),
      setFeedType: (feedType) => set({ feedType }),
      clearSession: () => set({ session: null, feedType: "global" }),
    }),
    { name: "nexus-auth" }
  )
);