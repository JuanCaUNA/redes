import React from "react";

interface ModalMessageProps {
  isOpen: boolean;
  type: "error" | "success";
  message: string;
  onClose: () => void;
}

const ModalMessage: React.FC<ModalMessageProps> = ({
  isOpen,
  type,
  message,
  onClose,
}) => {
  if (!isOpen) return null;

  const icon = type === "error" ? "❌" : "✅";
  const color = type === "error" ? "red" : "green";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm"></div>

      <div
        className={`relative z-10 bg-white rounded-xl p-6 shadow-lg w-[320px] text-center border border-${color}-300`}
      >
        <div className={`text-4xl mb-2 text-${color}-500`}>{icon}</div>
        <p className="text-gray-800 mb-4">{message}</p>
        <button
          onClick={onClose}
          className={`bg-${color}-500 hover:bg-${color}-600 text-white px-6 py-2 rounded transition`}
        >
          Cerrar
        </button>
      </div>
    </div>
  );
};

export default ModalMessage;
