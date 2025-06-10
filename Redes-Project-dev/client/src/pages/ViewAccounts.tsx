import React, { useEffect, useState } from "react";
import AccountModal from "../components/ModalMessage";

interface Transaction {
  type: "credit" | "debit";
  amount: number;
  currency: string;
  date: string;
}

interface AccountSummary {
  id: number;
  number: string;
  balance: number;
}

interface AccountDetails {
  id: number;
  number: string;
  currency: string;
  registeredBalance: number;
  calculatedBalance: number;
  transactions: Transaction[];
}

const ViewAccounts: React.FC = () => {
  const API_URL = import.meta.env.VITE_API_URL;
  const [accounts, setAccounts] = useState<AccountSummary[]>([]);
  const [username, setUsername] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedAccount, setSelectedAccount] = useState<AccountDetails | null>(
    null
  );
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const name = user?.name || "";
    setUsername(name);

    fetch(`${API_URL}/accounts?user=${encodeURIComponent(name)}`)
      .then((res) => {
        if (!res.ok) throw new Error("No se pudo cargar cuentas");
        return res.json();
      })
      .then((data) => setAccounts(data))
      .catch((err) => {
        console.error("Error al cargar cuentas:", err);
        setError("Hubo un problema al cargar las cuentas.");
      })
      .finally(() => setLoading(false));
  }, [API_URL]);

  const openModal = async (account: AccountSummary) => {
    try {
      const res = await fetch(`${API_URL}/accounts/${account.number}/details`);
      if (!res.ok) throw new Error("No se pudo obtener detalles de la cuenta");
      const data: AccountDetails = await res.json();
      setSelectedAccount(data);
      setModalOpen(true);
    } catch (err) {
      console.error("Error al cargar detalles de cuenta:", err);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4 text-center text-blue-800">
        Cuentas Registradas
      </h2>

      {loading ? (
        <p className="text-gray-600 text-center">Cargando cuentas...</p>
      ) : error ? (
        <p className="text-red-600 text-center">{error}</p>
      ) : accounts.length === 0 ? (
        <p className="text-gray-600 text-center">
          No hay cuentas registradas todavía.
        </p>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {accounts.map((acc) => (
            <div
              key={acc.id}
              onClick={() => openModal(acc)}
              className="bg-white p-4 rounded-xl shadow-md border border-gray-200 cursor-pointer hover:shadow-lg transition"
            >
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-semibold text-gray-700">
                    {username}
                  </h3>
                  <p className="text-sm text-gray-500">
                    N° Cuenta: {acc.number}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-400">Saldo:</p>
                  <p className="text-xl font-bold text-green-600">
                    ₡{acc.balance.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <AccountModal
        isOpen={modalOpen}
        data={selectedAccount}
        username={username}
        onClose={() => setModalOpen(false)}
      />
    </div>
  );
};

export default ViewAccounts;
