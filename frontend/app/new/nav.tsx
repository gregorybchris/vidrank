"use client";

import { cn } from "@/lib/utilities/style-utilities";
import { List, MonitorPlay, X } from "@phosphor-icons/react";
import Link from "next/link";
import { useState } from "react";

type NavProps = {
  children: React.ReactNode;
};

export function Nav({ children }: NavProps) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="">
      <NavBar menuOpen={menuOpen} setMenuOpen={setMenuOpen} />

      <div className="absolute h-full w-full">
        <div
          className={cn(
            "tracking-light absolute w-full px-5",
            !menuOpen && "invisible opacity-0",
          )}
        >
          <div className="flex flex-col gap-1 pt-10 text-2xl md:text-center md:text-3xl">
            <Link href="/new" onClick={() => setMenuOpen(false)}>
              <div className="px-1 py-2 hover:underline">Home</div>
            </Link>
            <Link href="/new/selection" onClick={() => setMenuOpen(false)}>
              <div className="px-1 py-2 hover:underline">Selection</div>
            </Link>
            <Link href="/new/rankings" onClick={() => setMenuOpen(false)}>
              <div className="px-1 py-2 hover:underline">Rankings</div>
            </Link>
            <Link href="/new/settings" onClick={() => setMenuOpen(false)}>
              <div className="px-1 py-2 hover:underline">Settings</div>
            </Link>
          </div>
        </div>

        <div className={cn("w-full", menuOpen && "invisible opacity-0")}>
          {children}
        </div>
      </div>
    </div>
  );
}

type NavBarProps = {
  menuOpen: boolean;
  setMenuOpen: (value: boolean) => void;
};

export function NavBar({ menuOpen, setMenuOpen }: NavBarProps) {
  return (
    <div className="flex flex-row items-center justify-between">
      <Link href="/new" onClick={() => setMenuOpen(false)}>
        <div className="p-4">
          <MonitorPlay size={40} color="#5086C9" />
        </div>
      </Link>

      {menuOpen ? (
        <div className="cursor-pointer p-5" onClick={() => setMenuOpen(false)}>
          <X size={32} />
        </div>
      ) : (
        <div className="cursor-pointer p-5" onClick={() => setMenuOpen(true)}>
          <List size={32} />
        </div>
      )}
    </div>
  );
}
