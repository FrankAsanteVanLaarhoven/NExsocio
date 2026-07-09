"use client";

import type { UserMode } from "@nexus/types";
import { cn } from "../utils";

const modeStyles: Record<UserMode, string> = {
  kids: "bg-[#7C4DFF]/15 text-[#B388FF] border-[#7C4DFF]/30",
  prime: "bg-[#00E5FF]/15 text-[#00E5FF] border-[#00E5FF]/30",
  professional: "bg-[#4FC3F7]/15 text-[#4FC3F7] border-[#4FC3F7]/30",
};

const modeLabels: Record<UserMode, string> = {
  kids: "Kids",
  prime: "Prime",
  professional: "Professional",
};

export function ModeBadge({ mode, className }: { mode: UserMode; className?: string }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest border",
        modeStyles[mode],
        className
      )}
    >
      {modeLabels[mode]}
    </span>
  );
}