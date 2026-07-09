import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["@nexus/ui", "@nexus/types"],
  experimental: {
    optimizePackageImports: ["@nexus/ui", "framer-motion"],
  },
};

export default nextConfig;