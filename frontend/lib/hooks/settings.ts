/* eslint-disable react-hooks/exhaustive-deps */
import { Settings } from "@/lib/models/settings";
import { deepEqual } from "@/lib/utilities/objectUtilities";
import { DependencyList, useEffect, useState } from "react";
import { useLocalStorage } from "usehooks-ts";

export function useSettings(dependencies: DependencyList) {
  const [storage, setStorage] = useLocalStorage<Settings | null>(
    "vidrank-settings",
    null,
  );
  const [settings, setSettings] = useState<Settings | null>(null);

  useEffect(() => {
    // Hydrate settings from storage
    if (settings === null && storage !== null) {
      setSettings(storage);
      console.log("Set settings to storage", storage);
    }
    /// Save to storage for the first time
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
  }, [settings, storage, setStorage]);

  return [settings, setSettings] as const;
}
