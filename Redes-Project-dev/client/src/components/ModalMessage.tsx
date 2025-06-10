import React from "react";

interface Transaction {
  type: "credit" | "debit";
  amount: number;
  currency: string;
  date: string;
}

interface AccountDetails {
  id: number;
  number: string;
  currency: string;
  registeredBalance: number;
  calculatedBalance: number;
  transactions: Transaction[];
}

interface Props {
  isOpen: boolean;
  data: AccountDetails | null;
  username: string;
  onClose: () => void;
}

const AccountModal: React.FC<Props> = ({ isOpen, data, username, onClose }) => {
  if (!isOpen || !data) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div
        className="absolute inset-0 bg-black/40 backdrop-blur-sm"
        onClick={onClose}
      ></div>
      <div className="relative z-10 bg-white rounded-xl p-6 shadow-lg w-[600px] max-h-[90vh] overflow-y-auto">
        <h2 className="text-xl font-bold text-blue-800 mb-2 text-center">
          Detalles de Cuenta
        </h2>
        <div className="text-center text-gray-700 mb-4">
          <p>
            <strong>Usuario:</strong> {username}
          </p>
          <p>
            <strong>Número:</strong> {data.number}
          </p>
          <p>
            <strong>Saldo registrado:</strong> ₡
            {data.registeredBalance.toLocaleString()}
          </p>
        </div>

        <table className="w-full text-sm mb-4 border border-gray-200">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-2 py-2 border">Tipo</th>
              <th className="px-2 py-2 border">Monto</th>
              <th className="px-2 py-2 border">Fecha</th>
            </tr>
          </thead>
          <tbody>
            {data.transactions.map((tx, index) => (
              <tr
                key={index}
                className={
                  tx.type === "credit" ? "text-green-600" : "text-red-600"
                }
              >
                <td className="px-2 py-1 border text-center">
                  {tx.type === "credit" ? "Crédito" : "Débito"}
                </td>
                <td className="px-2 py-1 border text-right">
                  {tx.type === "credit" ? "+" : "-"}₡
                  {Number(tx.amount).toLocaleString()}
                </td>
                <td className="px-2 py-1 border text-center">
                  {new Date(tx.date).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        <div className="text-center font-semibold text-blue-700 border-t pt-2">
          Saldo calculado: ₡{data.registeredBalance.toLocaleString()}
        </div>

        <div className="flex justify-center mt-4">
          <button
            onClick={onClose}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded transition"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
};

export default AccountModal;
