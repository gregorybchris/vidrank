import { Rankings } from "@/components/Rankings";
import { Dogear } from "widgets/Dogear";

export default function RankPage() {
  return (
    <div className="flex h-screen bg-stone-100">
      <div className="flex h-screen w-screen flex-col font-manrope text-stone-800">
        <Rankings />
      </div>

      <Dogear link="/" icon="videos" />
    </div>
  );
}
