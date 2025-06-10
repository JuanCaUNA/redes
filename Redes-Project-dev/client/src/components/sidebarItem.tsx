import React from "react";

interface SidebarItemProps {
  id: string;
  label: string;
  title?: string;
  image?: string | null;
  link?: string;
  isActive: boolean;
  onClick: (id: string) => void;
}

export const SidebarItem: React.FC<SidebarItemProps> = ({
  id,
  label,
  title,
  image,
  link,
  isActive,
  onClick,
}) => {
  return (
    <button
      onClick={() => onClick(id)}
      className={`w-full text-left flex items-center gap-3 py-3 px-4 rounded-md font-medium transition ${
        isActive ? "bg-blue-100 text-blue-700" : "text-gray-700 hover:bg-gray-100"
      }`}
    >
      {/* Imagen o ícono */}
      {image && (
        <img src={image} alt={`${label} icon`} className="w-6 h-6 object-cover rounded" />
      )}

      <div className="text-left flex-1">
        <div className="text-sm font-semibold">{label}</div>
        {title && <div className="text-xs text-gray-500">{title}</div>}
        {link && <div className="text-[10px] text-blue-500 truncate">{link}</div>}
      </div>
    </button>
  );
};
