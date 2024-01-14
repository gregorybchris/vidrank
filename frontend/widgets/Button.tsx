import { cn } from "@/lib/styleUtilities";

type ButtonProps = {
  className?: string;
  text: string;
  onClick: () => void;
  enabled?: boolean;
};

export function Button({ className, text, onClick, enabled }: ButtonProps) {
  const isEnabled = enabled ?? true;

  function handleClick() {
    if (!isEnabled) return;
    onClick();
  }

  return (
    <div
      className={cn(
        "select-none rounded px-4 py-1 tracking-wider transition-all",
        isEnabled
          ? "cursor-pointer text-stone-700 hover:bg-stone-300 hover:text-stone-800"
          : "text-stone-400",
        className,
      )}
      onClick={handleClick}
    >
      {text}
    </div>
  );
}
