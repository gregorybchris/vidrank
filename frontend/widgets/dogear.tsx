"use client";

import { CheckCircle, ListNumbers } from "@phosphor-icons/react";

import { cn } from "@/lib/utilities/style-utilities";
import styles from "@/styles/dogear.module.css";
import Link from "next/link";
import { match } from "ts-pattern";

type IconType = "rank" | "videos";

type DogearProps = {
  className?: string;
  link: string;
  icon: IconType;
};

export function Dogear({ className, link, icon }: DogearProps) {
  function getIcon() {
    if (icon == "rank") {
      return <ListNumbers size={28} color="#f8f8f8" weight="duotone" />;
    }
    if (icon == "videos") {
      return <CheckCircle size={28} color="#f8f8f8" weight="duotone" />;
    }
  }

  return (
    <Link href={link}>
      <div className="absolute -right-0 -top-0">
        <div
          className={cn(
            match(icon)
              .with("rank", () => "bg-blue-500 hover:bg-blue-600")
              .with("videos", () => "bg-red-500 hover:bg-red-600")
              .exhaustive(),
            "relative h-20 w-20 drop-shadow-md transition-all hover:drop-shadow-lg",
          )}
        >
          <div
            className={cn(
              "cursor-pointer select-none",
              "absolute z-10 h-full w-full",
              styles.dogear,
              className,
            )}
          >
            <div className="absolute bottom-2 left-2">{getIcon()}</div>
          </div>
        </div>
      </div>
    </Link>
  );
}
