/* eslint-disable react-hooks/exhaustive-deps */
import { Settings } from "@/lib/models/settings";
import { deepEqual } from "@/lib/utilities/objectUtilities";
import { useEffect, useState } from "react";
import { useLocalStorage } from "usehooks-ts";

export function useSettings() {
  const [storage, setStorage] = useLocalStorage<Settings | null>(
    "vidrank-settings",
    null,
  );
  const [settings, setSettings] = useState<Settings | null>(null);

  useEffect(() => {
    // Initialize settings and storage
    if (settings === null && storage === null) {
      const defaultSettings: Settings = {
        matching_settings: {
          by_date_strategy: null,
          by_rating_strategy: null,
          finetune_strategy: null,
          random_strategy: {},
        },
      };
      setSettings(defaultSettings);
      setStorage(defaultSettings);
      console.log("Set storage to settings", settings);
    }
    // Save to storage for the first time
    else if (settings !== null && storage === null) {
      setStorage(settings);
      console.log("Set storage to settings", settings);
    }
    // Overwrite storage with settings if they are different
    else if (
      settings !== null &&
      storage !== null &&
      !deepEqual(settings, storage)
    ) {
      setStorage(settings);
      console.log(
        "Overwrote storage with settings, storage",
        storage,
        "settings",
        settings,
      );
    }
  }, [settings]);

  useEffect(() => {
    // Hydrate settings from storage
    if (settings === null && storage !== null) {
      setSettings(storage);
      console.log("Set settings to storage", storage);
    }
  }, [storage, setStorage]);

  return [settings, setSettings] as const;
}
