import { Selector } from "@/components/Selector";

export default function Home() {
  return (
    <div className="flex h-screen bg-stone-100">
      <div className="w-screen h-screen flex flex-col justify-center items-center text-stone-800 font-roboto">
        <Selector />
      </div>
    </div>
  );
}
