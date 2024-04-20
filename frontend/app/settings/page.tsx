"use client";

import { useSettings } from "@/lib/hooks/settings";
import { cn } from "@/lib/utilities/styleUtilities";
import { ClockCountdown } from "@phosphor-icons/react";
import { Button } from "widgets/Button";
import { Dogear } from "widgets/Dogear";
import { SettingsButton } from "widgets/SettingsButton";

export default function SettingsPage() {
  const [settings, setSettings] = useSettings([]);

  const loading = settings === null;

  return (
    <div className="flex h-screen bg-stone-100">
      <div className="flex h-screen w-screen flex-col items-center justify-center space-y-8 font-manrope text-stone-800">
        {loading && (
          <div className="flex h-full flex-col items-center justify-center space-y-5 text-stone-600">
            <div className="text-4xl font-bold">Loading</div>
            <ClockCountdown size={80} color="#3e8fda" />
          </div>
        )}
        {!loading && (
          <>
            <div className="text-3xl text-stone-600">Settings</div>
            <div className="flex flex-col items-center space-y-2">
              <div className="text-lg font-bold">Matching Strategy</div>

              <div className="flex flex-row justify-center space-x-2">
                <Button
                  className={cn(
                    "text-sm transition-all",
                    settings.matchingStrategy === "balanced" &&
                      "bg-stone-300 text-stone-800",
                  )}
                  text="Balanced"
                  onClick={() =>
                    setSettings({ ...settings, matchingStrategy: "balanced" })
                  }
                />
                <Button
                  className={cn(
                    "text-sm transition-all",
                    settings.matchingStrategy === "random" &&
                      "bg-stone-300 text-stone-800",
                  )}
                  text="Random"
                  onClick={() =>
                    setSettings({ ...settings, matchingStrategy: "random" })
                  }
                />
                <Button
                  className={cn(
                    "text-sm transition-all",
                    settings.matchingStrategy === "by_rating" &&
                      "bg-stone-300 text-stone-800",
                  )}
                  text="By Rating"
                  onClick={() =>
                    setSettings({ ...settings, matchingStrategy: "by_rating" })
                  }
                />
              </div>
            </div>
          </>
        )}
      </div>

      <Dogear link="/" icon="videos" />

      <SettingsButton />
    </div>
  );
}
