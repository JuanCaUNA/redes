import React, { useEffect, useState } from "react";

interface Account {
  id: string;
  number: string;
  currency: string;
}

const PhoneLinkPage: React.FC = () => {
  const API_URL = import.meta.env.VITE_API_URL;
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [selectedAccount, setSelectedAccount] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [userName, setUserName] = useState(""); // NUEVO
  const [message, setMessage] = useState("");

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const username = user?.name || "";
    setUserName(username); // GUARDAMOS EL USERNAME

    fetch(`${API_URL}/accounts?user=${encodeURIComponent(username)}`)
      .then((res) => res.json())
      .then((data: Account[]) => {
        setAccounts(data);
        if (data.length > 0) setSelectedAccount(data[0].number);
      })
      .catch(() => {
        setMessage("Error al cargar tus cuentas.");
      });
  }, [API_URL]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedAccount || !phoneNumber.match(/^(\+506)?[0-9]{8}$/)) {
      setMessage("Debes ingresar un número de teléfono válido.");
      return;
    }

    try {
      const res = await fetch(`${API_URL}/phone-link`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          account_number: selectedAccount,
          phone: phoneNumber,
          user_name: userName, // SE ENVÍA AL BACKEND
        }),
      });

      const result = await res.json();

      if (!res.ok) throw new Error(result.error || "Error desconocido");

      setMessage("Cuenta asociada exitosamente.");
    } catch (err: unknown) {
      if (err && typeof err === "object" && "message" in err) {
        setMessage((err as { message: string }).message);
      } else {
        setMessage("Error desconocido");
      }
    }
  };

  return (
    <div className="max-w-xl mx-auto bg-white p-8 rounded-xl shadow-md mt-10 space-y-6">
      <h2 className="text-2xl font-bold text-center text-blue-800">
        Asociar Cuenta a Teléfono
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Selecciona una cuenta
          </label>
          <select
            value={selectedAccount}
            onChange={(e) => setSelectedAccount(e.target.value)}
            className="w-full rounded-md border-gray-300 px-4 py-3 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          >
            {accounts.map((acc) => (
              <option key={acc.id} value={acc.number}>
                {acc.number} ({acc.currency})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Número de teléfono (ej: 88888888)
          </label>
          <input
            type="tel"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            placeholder="Número sin prefijo internacional"
            className="w-full rounded-md border-gray-300 px-4 py-3 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 font-semibold transition"
        >
          Asociar Teléfono
        </button>
      </form>

      {message && (
        <p className="text-center text-sm text-gray-700 mt-4">{message}</p>
      )}
    </div>
  );
};

export default PhoneLinkPage;
