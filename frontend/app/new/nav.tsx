"use client";

import { List, X } from "@phosphor-icons/react";
import Link from "next/link";
import { useState } from "react";

type RootLayoutProps = {
  children: React.ReactNode;
};

export function Nav({ children }: RootLayoutProps) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="">
      <div className="flex flex-row justify-end">
        {menuOpen ? (
          <div
            className="cursor-pointer p-1"
            onClick={() => setMenuOpen(false)}
          >
            <X size={32} />
          </div>
        ) : (
          <div className="cursor-pointer p-1" onClick={() => setMenuOpen(true)}>
            <List size={32} />
          </div>
        )}
      </div>

      {menuOpen ? (
        <div className="flex flex-col gap-1 text-xl md:text-2xl">
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
      ) : (
        <>{children}</>
      )}
    </div>
  );
}
