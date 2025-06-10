import React from "react";
import { useNavigate } from "react-router-dom";
import { FiLogOut } from "react-icons/fi";
import { SidebarItem } from "./sidebarItem";

interface Section {
  id: string;
  label: string;
  title?: string;
  image?: string | null;
  link?: string;
  isActive: boolean;
  onClick: () => void;
}

interface SidebarProps {
  sections: Section[];
}

export const Sidebar: React.FC<SidebarProps> = ({ sections }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    navigate("/", { replace: true });
    window.location.reload(); // ← fuerza que se vuelva a montar `Login`
    localStorage.removeItem("user"); // Limpia el usuario del localStorage
  };

  return (
    <aside className="w-full max-w-xs bg-white p-6 border-r border-gray-200 h-screen fixed left-0 top-0 shadow-md flex flex-col justify-between">
      <nav className="space-y-2">
        {sections.map((section) => (
          <SidebarItem
            key={section.id}
            id={section.id}
            label={section.label}
            title={section.title}
            image={section.image}
            link={section.link}
            isActive={section.isActive}
            onClick={() => section.onClick()}
          />
        ))}
      </nav>

      <button
        onClick={handleLogout}
        className="mt-6 flex items-center justify-center gap-2 w-full bg-red-500 hover:bg-red-600 text-white py-2 rounded text-sm font-semibold transition-colors"
      >
        <FiLogOut size={18} />
        Cerrar sesión
      </button>
    </aside>
  );
};
