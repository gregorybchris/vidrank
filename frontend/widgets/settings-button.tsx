"use client";

import { Gear } from "@phosphor-icons/react";

import { cn } from "@/lib/utilities/style-utilities";
import Link from "next/link";

type SettingsButtonProps = {
  className?: string;
};

export function SettingsButton({ className }: SettingsButtonProps) {
  return (
    <Link href="/settings">
      <div className={cn("absolute bottom-3 right-3", className)}>
        <div className="p-3">
          <Gear size={28} color="#505050" weight="duotone" />
        </div>
      </div>
    </Link>
  );
}
