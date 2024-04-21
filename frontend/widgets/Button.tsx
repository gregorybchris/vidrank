import { cn } from "@/lib/utilities/styleUtilities";

type ButtonProps = {
  className?: string;
  text: string;
  onClick: () => void;
  enabled?: boolean;
  onClickDisabled?: () => void;
};

export function Button({
  className,
  text,
  onClick,
  enabled,
  onClickDisabled,
}: ButtonProps) {
  const isEnabled = enabled ?? true;

  function handleClick() {
    if (isEnabled) {
      onClick();
    } else {
      onClickDisabled && onClickDisabled();
    }
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
