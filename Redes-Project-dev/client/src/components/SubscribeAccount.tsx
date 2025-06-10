import React, { useState } from "react";

const SubscribeAccount: React.FC = () => {
  const [accountNumber, setAccountNumber] = useState("");
  const [subscriberName, setSubscriberName] = useState("");
  const [currency, setCurrency] = useState("CRC");
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!accountNumber || !subscriberName) {
      setMessage("Por favor, complete todos los campos.");
      return;
    }

    setMessage(
      `Suscripción realizada exitosamente para ${subscriberName} en la cuenta ${accountNumber} en ${
        currency === "CRC" ? "colones" : "dólares"
      }.`
    );

    setAccountNumber("");
    setSubscriberName("");
    setCurrency("CRC");
  };

  return (
    <div className="h-full flex items-center justify-center">
      <div className="w-full max-w-xl bg-white shadow-lg rounded-xl p-8">
        <h2 className="text-2xl font-bold text-blue-800 mb-6 text-center">
          Suscripción a Cuentas
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Número de cuenta
            </label>
            <input
              type="text"
              value={accountNumber}
              onChange={(e) => setAccountNumber(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500 text-base px-4 py-3"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Nombre del suscriptor
            </label>
            <input
              type="text"
              value={subscriberName}
              onChange={(e) => setSubscriberName(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500 text-base px-4 py-3"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Moneda
            </label>
            <select
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500 text-base px-4 py-3"
            >
              <option value="CRC">₡ Colones (CRC)</option>
              <option value="USD">$ Dólar (USD)</option>
              <option value="EUR">€ Euro (EUR)</option>
              <option value="GBP">£ Libra esterlina (GBP)</option>
              <option value="JPY">¥ Yen japonés (JPY)</option>
              <option value="CNY">¥ Yuan chino (CNY)</option>
              <option value="MXN">$ Peso mexicano (MXN)</option>
              <option value="BRL">R$ Real brasileño (BRL)</option>
              <option value="CAD">$ Dólar canadiense (CAD)</option>
              <option value="ARS">$ Peso argentino (ARS)</option>
            </select>
          </div>

          <button
            type="submit"
            className="w-full bg-green-600 text-white font-semibold py-3 rounded-md hover:bg-green-700 transition text-base"
          >
            Suscribirse
          </button>
        </form>

        {message && (
          <div className="mt-6 text-center text-green-700 font-medium text-base">
            {message}
          </div>
        )}
      </div>
    </div>
  );
};

export default SubscribeAccount;
