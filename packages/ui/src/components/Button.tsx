"use client";

import { cn } from "../utils";

type ButtonVariant = "primary" | "secondary" | "ghost" | "danger";
type ButtonSize = "sm" | "md" | "lg";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
}

const variants: Record<ButtonVariant, string> = {
  primary:
    "bg-[#00E5FF] text-[#0A0A0A] hover:bg-[#33EBFF] border border-[#00E5FF]/50 shadow-[0_0_20px_rgba(0,229,255,0.2)]",
  secondary:
    "bg-[#1A1A1A] text-[#F5F5F5] hover:bg-[#222] border border-[#2A2A2A]",
  ghost: "bg-transparent text-[#8A8A8A] hover:text-[#F5F5F5] hover:bg-[#1A1A1A]/50",
  danger: "bg-[#FF5252]/10 text-[#FF5252] border border-[#FF5252]/30 hover:bg-[#FF5252]/20",
};

const sizes: Record<ButtonSize, string> = {
  sm: "px-3 py-1.5 text-xs",
  md: "px-4 py-2 text-sm",
  lg: "px-6 py-3 text-base",
};

export function Button({
  variant = "primary",
  size = "md",
  loading,
  className,
  children,
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-md font-medium tracking-wide transition-all active:scale-[0.98]",
        "disabled:opacity-50 disabled:cursor-not-allowed",
        variants[variant],
        sizes[size],
        className
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
      ) : null}
      {children}
    </button>
  );
}