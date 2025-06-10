import React, { useState, useEffect } from "react";

const CreateAccountForm: React.FC = () => {
  const API_URL = import.meta.env.VITE_API_URL;
  const [number, setNumber] = useState("");
  const [currency, setCurrency] = useState("CRC");
  const [balance, setBalance] = useState("");
  const [userId, setUserId] = useState("");
  const [users, setUsers] = useState<{ id: number; name: string }[]>([]);

  // Cargar usuarios (excluyendo Admin)
  useEffect(() => {
    fetch(`${API_URL}/users`)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setUsers(data);
        } else if (Array.isArray(data.users)) {
          setUsers(data.users);
        } else {
          throw new Error("Respuesta inesperada al cargar usuarios.");
        }
      })
      .catch((err) => {
        console.error("Error al cargar usuarios:", err);
        alert("Error cargando usuarios.");
      });
  }, [API_URL]);

  // Obtener número de cuenta IBAN generado automáticamente
  useEffect(() => {
    fetch(`${API_URL}/accounts/iban`)
      .then((res) => res.json())
      .then((data) => {
        if (data.iban) {
          setNumber(data.iban);
        } else {
          throw new Error("No se pudo obtener el número IBAN.");
        }
      })
      .catch((err) => {
        console.error("Error generando número IBAN:", err);
        alert("Error generando número de cuenta.");
      });
  }, [API_URL]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const parsedUserId = Number(userId);
    const parsedBalance = Number(balance);

    if (
      !number ||
      !currency ||
      isNaN(parsedBalance) ||
      isNaN(parsedUserId) ||
      parsedUserId <= 0
    ) {
      alert("Todos los campos son obligatorios y válidos.");
      return;
    }

    const payload = {
      number,
      currency,
      balance: parsedBalance,
      user_id: parsedUserId,
    };

    console.log("📤 Enviando:", payload);

    try {
      const response = await fetch(`${API_URL}/accounts`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const result = await response.json();

      if (!response.ok) {
        alert("Error al crear la cuenta: " + result.error);
        return;
      }

      alert("✅ Cuenta creada exitosamente");

      // Limpiar campos
      setBalance("");
      setUserId("");

      // Obtener nuevo IBAN
      const next = await fetch(`${API_URL}/accounts/iban`).then((res) =>
        res.json()
      );
      setNumber(next.iban || "");
    } catch (err) {
      console.error("Error al crear la cuenta:", err);
      alert("No se pudo conectar con el servidor.");
    }
  };

  return (
    <div className="h-full flex items-center justify-center">
      <div className="w-full max-w-xl bg-white shadow-lg rounded-xl p-8">
        <h2 className="text-2xl font-bold text-blue-800 mb-6 text-center">
          Crear Cuenta
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Número de cuenta (IBAN)
            </label>
            <input
              type="text"
              value={number}
              readOnly
              className="mt-1 block w-full bg-gray-100 border border-gray-300 rounded-md shadow-sm"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Moneda
            </label>
            <select
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="CRC">CRC</option>
              <option value="USD">USD</option>
              <option value="EUR">EUR</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Saldo inicial
            </label>
            <input
              type="number"
              value={balance}
              onChange={(e) => setBalance(e.target.value)}
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Asignar a usuario
            </label>
            <select
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Seleccione un usuario</option>
              {users.map((u) => (
                <option key={u.id} value={String(u.id)}>
                  {u.name}
                </option>
              ))}
            </select>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white font-semibold py-2 rounded-md hover:bg-blue-700 transition"
          >
            Agregar Cuenta
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreateAccountForm;
