"use client";

import { useReducedMotion } from "framer-motion";
import { useEffect, useRef } from "react";

type SplashVideoProps = {
  className?: string;
  variant?: "hero" | "phone";
};

export function SplashVideo({ className = "", variant = "hero" }: SplashVideoProps) {
  const reduceMotion = useReducedMotion();
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video || reduceMotion) return;

    const play = () => {
      void video.play().catch(() => {
        /* autoplay may be blocked until user gesture */
      });
    };

    play();
    video.addEventListener("loadeddata", play);
    return () => video.removeEventListener("loadeddata", play);
  }, [reduceMotion]);

  const isPhone = variant === "phone";

  return (
    <video
      ref={videoRef}
      className={`block h-full w-full ${isPhone ? "object-cover" : "object-contain"} ${className}`}
      src="/splash-nexsocio.mp4"
      poster="/brand-splash-reference.jpg"
      autoPlay={!reduceMotion}
      loop={!reduceMotion}
      muted
      playsInline
      preload="auto"
      aria-label="NexSocio liquid logo animation"
    />
  );
}