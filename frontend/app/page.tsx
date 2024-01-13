import { Selector } from "@/components/Selector";

export default function Home() {
  return (
    <div className="flex h-screen bg-stone-100">
      <div className="flex h-screen w-screen flex-col items-center justify-center font-manrope text-stone-800">
        <Selector />
      </div>
    </div>
  );
}
