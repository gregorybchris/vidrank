"use client";

import { useSettings } from "@/lib/hooks/settings";
import { MatchingStrategy } from "@/lib/models/matchingStrategy";
import { cn } from "@/lib/utilities/styleUtilities";
import { ClockCountdown } from "@phosphor-icons/react";
import { useEffect, useState } from "react";
import { Button } from "widgets/Button";
import { Dogear } from "widgets/Dogear";
import { SettingsButton } from "widgets/SettingsButton";

export default function SettingsPage() {
  const [settings, setSettings] = useSettings();
  const [randomFractionInput, setRandomFractionInput] = useState<number>(0.5);

  const loading = settings === null;

  useEffect(() => {
    if (settings === null) return;
    setRandomFractionInput(settings.matching_settings.balanced_random_fraction);
  }, [settings]);

  function updateMatchingStrategy(strategy: MatchingStrategy) {
    setSettings((settings) => {
      if (settings === null) return settings;
      const settingsCopy = { ...settings };
      settingsCopy.matching_settings.matching_strategy = strategy;
      return settingsCopy;
    });
  }

  function updateRandomFraction(randomFraction: number) {
    setSettings((settings) => {
      if (settings === null) return settings;
      const settingsCopy = { ...settings };
      settingsCopy.matching_settings.balanced_random_fraction = randomFraction;
      return settingsCopy;
    });
  }

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
              <div className="text-lg font-bold">Matching strategy</div>

              <div className="flex flex-row justify-center space-x-2">
                <Button
                  className={cn(
                    "text-sm transition-all",
                    settings.matching_settings.matching_strategy ===
                      "balanced" && "bg-stone-300 text-stone-800",
                  )}
                  text="Balanced"
                  onClick={() => updateMatchingStrategy("balanced")}
                />
                <Button
                  className={cn(
                    "text-sm transition-all",
                    settings.matching_settings.matching_strategy === "random" &&
                      "bg-stone-300 text-stone-800",
                  )}
                  text="Random"
                  onClick={() => updateMatchingStrategy("random")}
                />
                <Button
                  className={cn(
                    "text-sm transition-all",
                    settings.matching_settings.matching_strategy ===
                      "by_rating" && "bg-stone-300 text-stone-800",
                  )}
                  text="By rating"
                  onClick={() => updateMatchingStrategy("by_rating")}
                />
              </div>

              {settings.matching_settings.matching_strategy == "balanced" && (
                <div className="flex flex-row items-center space-x-2 text-sm">
                  <div className="font-bold">Balanced random fraction:</div>
                  <input
                    className="w-16 rounded bg-transparent px-2 py-1 outline-none"
                    type="number"
                    step={0.05}
                    min={0}
                    max={1}
                    value={randomFractionInput}
                    onChange={(e) => {
                      const newValue = parseFloat(e.target.value);
                      setRandomFractionInput(newValue);
                      updateRandomFraction(newValue);
                    }}
                  />
                </div>
              )}
            </div>
          </>
        )}
      </div>

      <Dogear link="/" icon="videos" />

      <SettingsButton />
    </div>
  );
}
