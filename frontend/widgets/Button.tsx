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
        "cursor-pointer rounded px-2 py-1 transition-all hover:bg-neutral-500",
        className,
      )}
      onClick={onClick}
    >
      <div className="select-none tracking-widest">{text}</div>
    </div>
  );
}
