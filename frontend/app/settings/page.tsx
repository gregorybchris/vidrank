"use client";

import { useSettings } from "@/lib/hooks/settings";
import { MatchingStrategy } from "@/lib/models/matching-strategy";
import { cn } from "@/lib/utilities/style-utilities";
import { ClockCountdown } from "@phosphor-icons/react";
import { useEffect, useState } from "react";
import { Button } from "widgets/button";
import { Dogear } from "widgets/dogear";
import { SettingsButton } from "widgets/settings-button";

export default function SettingsPage() {
  const [settings, setSettings] = useSettings();
  // const [matchingStrategy, setMatchingStrategy] =
  //   useState<MatchingStrategy>("random");
  const [finetuneFractionInput, setFinetuneFractionInput] =
    useState<number>(0.25);
  const [byDateDaysInput, setByDateDaysInput] = useState<number>(30);

  const loading = settings === null;

  useEffect(() => {
    if (settings === null) return;
    // Load the settings from storage into the React input state variables
    if (settings.matching_settings.finetune_strategy !== null) {
      setFinetuneFractionInput(
        settings.matching_settings.finetune_strategy.fraction,
      );
    }
    if (settings.matching_settings.by_date_strategy !== null) {
      setByDateDaysInput(settings.matching_settings.by_date_strategy.days);
    }
  }, [settings]);

  // TODO: This might help with the issue updating both settings and React inputs at the same time
  // useEffect(() => {
  //   updateMatchingSettings(matchingStrategy);
  //   // eslint-disable-next-line react-hooks/exhaustive-deps
  // }, [matchingStrategy, finetuneFractionInput, byDateDays]);

  function updateMatchingSettings(strategy: MatchingStrategy) {
    // setMatchingStrategy(strategy);
    setSettings((settings) => {
      if (settings === null) return settings;
      const settingsCopy = { ...settings };

      // Update the matching settings based on the React input state variables
      if (strategy === "by_date") {
        settingsCopy.matching_settings = {
          by_date_strategy: {
            days: byDateDaysInput,
          },
          by_rating_strategy: null,
          finetune_strategy: null,
          random_strategy: null,
        };
      } else if (strategy === "by_rating") {
        settingsCopy.matching_settings = {
          by_date_strategy: null,
          by_rating_strategy: {},
          finetune_strategy: null,
          random_strategy: null,
        };
      } else if (strategy === "finetune") {
        settingsCopy.matching_settings = {
          by_date_strategy: null,
          by_rating_strategy: null,
          finetune_strategy: {
            fraction: finetuneFractionInput,
          },
          random_strategy: null,
        };
      } else if (strategy === "random") {
        settingsCopy.matching_settings = {
          by_date_strategy: null,
          by_rating_strategy: null,
          finetune_strategy: null,
          random_strategy: {},
        };
      }
      return settingsCopy;
    });
  }

  function updateFinetuneFractionInput(finetuneFractionInput: number) {
    // Update the settings directly based on an updated finetune fraction input
    // TODO: Figure out how to remove this
    // We want to set the settings at the same time as the React input state variables
    setSettings((settings) => {
      if (settings === null) return settings;
      const settingsCopy = { ...settings };
      if (!settingsCopy.matching_settings.finetune_strategy) return settings;
      settingsCopy.matching_settings.finetune_strategy.fraction =
        finetuneFractionInput;
      return settingsCopy;
    });
  }

  function updateByDateDaysInput(byDateDays: number) {
    // Update the settings directly based on an updated by date days
    // TODO: Figure out how to remove this
    // We want to set the settings at the same time as the React input state variables
    setSettings((settings) => {
      if (settings === null) return settings;
      const settingsCopy = { ...settings };
      if (!settingsCopy.matching_settings.by_date_strategy) return settings;
      settingsCopy.matching_settings.by_date_strategy.days = byDateDays;
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
                    settings.matching_settings.random_strategy !== null &&
                      "bg-stone-300 text-stone-800",
                  )}
                  text="Random"
                  onClick={() => updateMatchingSettings("random")}
                />
                <Button
                  className={cn(
                    "text-sm transition-all",
                    settings.matching_settings.by_rating_strategy !== null &&
                      "bg-stone-300 text-stone-800",
                  )}
                  text="By rating"
                  onClick={() => updateMatchingSettings("by_rating")}
                />
                <Button
                  className={cn(
                    "text-sm transition-all",
                    settings.matching_settings.by_date_strategy !== null &&
                      "bg-stone-300 text-stone-800",
                  )}
                  text="By date"
                  onClick={() => updateMatchingSettings("by_date")}
                />
                <Button
                  className={cn(
                    "text-sm transition-all",
                    settings.matching_settings.finetune_strategy !== null &&
                      "bg-stone-300 text-stone-800",
                  )}
                  text="Finetune"
                  onClick={() => updateMatchingSettings("finetune")}
                />
              </div>

              {settings.matching_settings.finetune_strategy !== null && (
                <div className="flex flex-row items-center space-x-2 text-sm">
                  <div className="font-bold">Fraction:</div>
                  <input
                    className="w-16 rounded bg-transparent px-2 py-1 outline-none"
                    type="number"
                    step={0.05}
                    min={0}
                    max={1}
                    value={finetuneFractionInput}
                    onChange={(e) => {
                      const newValue = parseFloat(e.target.value);
                      setFinetuneFractionInput(newValue);
                      updateFinetuneFractionInput(newValue);
                    }}
                  />
                </div>
              )}

              {settings.matching_settings.by_date_strategy !== null && (
                <div className="flex flex-row items-center space-x-2 text-sm">
                  <div className="font-bold">Days:</div>
                  <input
                    className="w-16 rounded bg-transparent px-2 py-1 outline-none"
                    type="number"
                    step={1}
                    min={1}
                    value={byDateDaysInput}
                    onChange={(e) => {
                      let newValue = parseInt(e.target.value);
                      if (newValue < 1) newValue = 1;
                      setByDateDaysInput(newValue);
                      updateByDateDaysInput(newValue);
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
