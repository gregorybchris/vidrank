import { cn } from "@/lib/styleUtilities";

type ButtonProps = {
  className?: string;
  text: string;
  onClick: () => void;
};

export function Button({ className, text, onClick }: ButtonProps) {
  return (
    <div className="bg-stone-600 p-[3px] rounded">
      <div
        className={cn(
          "border-b-4 border-stone-600 rounded-sm bg-stone-500 w-20 text-center py-1 cursor-pointer transition-all active:bg-stone-500 active:border-t-4 active:border-stone-500 active:border-b-0",
          className
        )}
        onClick={onClick}
      >
        <span className="select-none font-bold text-stone-900">{text}</span>
      </div>
    </div>
  );
}
