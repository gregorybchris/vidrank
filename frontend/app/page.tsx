import { Selector } from "@/components/selector";
import { Dogear } from "widgets/dogear";
import { SettingsButton } from "widgets/settings-button";

export default function HomePage() {
  return (
    <div className="flex h-screen bg-stone-100">
      <div className="flex h-screen w-screen flex-col items-center justify-center font-manrope text-stone-800">
        <Selector />
      </div>

      <Dogear link="/rank" icon="rank" />

      <SettingsButton />
    </div>
  );
}
