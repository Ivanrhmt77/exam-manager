import { GraduationCap } from "lucide-react";

const AppLogo = () => {
  return (
    <div className="flex items-center gap-2.5">
      <div className="bg-primary-500 flex h-9 w-9 items-center justify-center rounded-lg">
        <GraduationCap size={20} className="text-white" />
      </div>
      <p className="type-headline-sm">ExamManager</p>
    </div>
  );
};

export default AppLogo;
