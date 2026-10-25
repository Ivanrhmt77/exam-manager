import type { LucideIcon } from "lucide-react";

type CardProps = {
  icon: LucideIcon;
  title: string;
  description: string;
};

const card = ({ icon: Icon, title, description }: CardProps) => {
  return (
    <div className="flex gap-3 rounded-xl border border-neutral-200 bg-white p-4">
      <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-neutral-200">
        <Icon size={17} className="text-primary-500" />
      </div>
      <div className="flex flex-col gap-0.5">
        <span className="text-sm font-semibold">{title}</span>
        <span className="text-xs text-neutral-500">{description}</span>
      </div>
    </div>
  );
};

export default card;
