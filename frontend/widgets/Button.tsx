import { cn } from "@/lib/styleUtilities";

type ButtonProps = {
  className?: string;
  text: string;
  onClick: () => void;
};

export function Button({ className, text, onClick }: ButtonProps) {
  return (
    <div
      className={cn(
        "cursor-pointer rounded-md px-3 py-1 transition-all hover:bg-stone-300",
        "select-none tracking-wider text-stone-600 hover:text-stone-800",
        className,
      )}
      onClick={onClick}
    >
      {text}
    </div>
  );
}
