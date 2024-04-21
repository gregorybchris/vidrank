import * as RadixToast from "@radix-ui/react-toast";

type ToastProps = {
  visible: boolean;
  setVisible: (visible: boolean) => void;
  title: string;
  description: string;
  buttonText: string;
};

export function Toast({
  visible,
  setVisible,
  title,
  description,
  buttonText,
}: ToastProps) {
  return (
    <RadixToast.Provider swipeDirection="right" duration={4000}>
      <RadixToast.Root
        className="data-[state=open]:animate-slideIn data-[state=closed]:animate-hide data-[swipe=end]:animate-swipeOut grid grid-cols-[auto_max-content] items-center gap-x-[15px] rounded-md bg-white p-[15px] shadow-xl [grid-template-areas:_'title_action'_'description_action'] data-[swipe=cancel]:translate-x-0 data-[swipe=move]:translate-x-[var(--radix-radixToast-swipe-move-x)] data-[swipe=cancel]:transition-[transform_200ms_ease-out]"
        open={visible}
        onOpenChange={setVisible}
      >
        <RadixToast.Title className="mb-[5px] text-[15px] font-medium [grid-area:_title]">
          {title}
        </RadixToast.Title>
        <RadixToast.Description asChild>
          <div className="m-0 text-[13px] leading-[1.3] [grid-area:_description]">
            {description}
          </div>
        </RadixToast.Description>
        <RadixToast.Action
          className="[grid-area:_action]"
          asChild
          altText="Goto schedule to undo"
        >
          <button className="inline-flex h-[25px] items-center justify-center rounded bg-blue-400/20 px-[10px] text-xs font-medium leading-[25px] text-blue-800 shadow-[inset_0_0_0_1px] transition-all hover:bg-blue-400/40 hover:shadow-[inset_0_0_0_1px] focus:shadow-[0_0_0_2px]">
            {buttonText}
          </button>
        </RadixToast.Action>
      </RadixToast.Root>
      <RadixToast.Viewport className="fixed bottom-0 right-0 z-[100] m-0 flex w-[390px] max-w-[100vw] list-none flex-col gap-[10px] p-[var(--viewport-padding)] outline-none [--viewport-padding:_25px]" />
    </RadixToast.Provider>
  );
}
