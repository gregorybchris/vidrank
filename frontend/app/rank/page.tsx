import { Rankings } from "@/components/rankings";
import { Dogear } from "widgets/dogear";
import { SettingsButton } from "widgets/settings-button";

export default function RankPage() {
  return (
    <div className="flex h-screen bg-stone-100">
      <div className="flex h-screen w-screen flex-col font-manrope text-stone-800">
        <Rankings />
      </div>

      <Dogear link="/" icon="videos" />

      <SettingsButton />
    </div>
  );
}
