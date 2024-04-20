import { Selector } from "@/components/Selector";
import { Dogear } from "widgets/Dogear";
import { SettingsButton } from "widgets/SettingsButton";

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
