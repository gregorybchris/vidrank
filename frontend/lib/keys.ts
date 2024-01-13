/* eslint-disable react-hooks/exhaustive-deps */
import { DependencyList, useEffect, useState } from "react";

export interface Combo {
  pattern: string;
  callback: () => void;
  preventDefault?: boolean;
}

export function useKeyCombos(
  combos: Combo[],
  dependencies: DependencyList,
): void {
  const [keys, setKeys] = useState<string[]>([]);

  function onDown(event: KeyboardEvent) {
    setKeys((keys) => {
      const newKey = event.key;
      if (keys.includes(newKey)) {
        return keys;
      }
      const newKeys = [...keys, newKey];
      const comboPattern = newKeys.join("+");
      for (let i = 0; i < combos.length; i++) {
        const combo = combos[i];
        if (comboPattern == combo.pattern) {
          if (combo.preventDefault ?? true) {
            event.preventDefault();
          }
          combo.callback();
          break;
        }
      }
      return newKeys;
    });
  }

  function onUp(event: KeyboardEvent) {
    const key = event.key;
    const metaKeys = ["Meta", "Shift", "Command", "Alt", "Control"];
    if (metaKeys.includes(key)) {
      setKeys([]);
    } else {
      setKeys((keys) =>
        keys.includes(key) ? keys.filter((k) => k != key) : keys,
      );
    }
  }

  useEffect(() => {
    window.addEventListener("keydown", onDown);
    window.addEventListener("keyup", onUp);

    return () => {
      window.removeEventListener("keydown", onDown);
      window.removeEventListener("keyup", onUp);
    };
  }, [dependencies]);
}
