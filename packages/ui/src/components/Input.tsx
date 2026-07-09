"use client";

import { cn } from "../utils";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export function Input({ label, error, hint, className, id, ...props }: InputProps) {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, "-");

  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label htmlFor={inputId} className="text-xs font-medium tracking-wider text-[#8A8A8A] uppercase">
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={cn(
          "w-full rounded-md border bg-[#0A0A0A] px-3 py-2.5 text-sm text-[#F5F5F5]",
          "border-[#2A2A2A] placeholder:text-[#5A5A5A]",
          "focus:outline-none focus:border-[#00E5FF]/50 focus:ring-1 focus:ring-[#00E5FF]/20",
          "transition-colors",
          error && "border-[#FF5252]/50",
          className
        )}
        {...props}
      />
      {hint && !error && <p className="text-xs text-[#5A5A5A]">{hint}</p>}
      {error && <p className="text-xs text-[#FF5252]">{error}</p>}
    </div>
  );
}