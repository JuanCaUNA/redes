import React, { useEffect, useState } from "react";
import ModalMessage from "./modal";

interface Account {
  id: string;
  number: string;
  currency: string;
  balance: number;
}

interface TransferData {
  fromAccount: string;
  phone: string;
  amount: number;
  currency: string;
  comment?: string;
}

interface Props {
  onContinue: (data: TransferData) => void;
}

const SinpeTransferForm: React.FC<Props> = ({ onContinue }) => {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [fromAccount, setFromAccount] = useState("");
  const [phone, setPhone] = useState("");
  const [amount, setAmount] = useState("");
  const [currency, setCurrency] = useState("CRC");
  const [comment, setComment] = useState("");
  const [receiverName, setReceiverName] = useState<string | null>(null);
  const [modalError, setModalError] = useState(false);
  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user") || "{}");

    fetch(`${API_URL}/sinpe/user-link/${user.name}`)
      .then((res) => res.json())
      .then((data) => {
        if (!data.linked) {
          alert("Ninguna de tus cuentas está vinculada a SINPE Móvil.");
          // Podés redirigir o desactivar el formulario
        } else {
          localStorage.setItem("senderInfo", data.phone);
          console.log("Sender info saved:", data.phone);
        }
      })
      .catch(() => {
        alert("Error al verificar si tu cuenta está vinculada a SINPE.");
      });
  }, [API_URL]);

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const username = user?.name || "";

    fetch(`${API_URL}/accounts?user=${encodeURIComponent(username)}`)
      .then((res) => res.json())
      .then((data: Account[]) => {
        setAccounts(data);
        if (data.length > 0) {
          setFromAccount(data[0].number);
          setCurrency(data[0].currency);
        }
      })
      .catch(() => {
        alert("Error al cargar cuentas");
      });
  }, [API_URL]);

  useEffect(() => {
    if (fromAccount) {
      const bankCode = fromAccount.slice(5, 8);
      localStorage.setItem("senderAccount", bankCode);
      console.log("Bank code saved:", bankCode);
    }
  }, [fromAccount]);

  useEffect(() => {
    const buscarNombre = async () => {
      if (!phone.match(/^[0-9]{8}$/)) {
        setReceiverName(null);
        return;
      }

      try {
        const res = await fetch(`${API_URL}/validate/${phone}`);
        if (!res.ok) throw new Error();
        const data = await res.json();
        console.log(data);
        localStorage.setItem("receiverInfo", JSON.stringify(data));
        setReceiverName(data.name);
      } catch {
        setReceiverName(null);
        setModalError(true);
      }
    };

    buscarNombre();
  }, [phone, API_URL]);

  const selectedAccount = accounts.find((acc) => acc.number === fromAccount);
  const isValidAmount = Number(amount) <= (selectedAccount?.balance ?? 0);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!phone.match(/^[0-9]{8}$/)) {
      alert("Ingrese un número de teléfono válido.");
      return;
    }

    if (!isValidAmount) {
      alert("Monto insuficiente.");
      return;
    }

    const transferData: TransferData = {
      fromAccount,
      phone,
      amount: Number(amount),
      currency,
      comment,
    };

    onContinue(transferData);
  };

  return (
    <>
      <form
        onSubmit={handleSubmit}
        className="space-y-6 max-w-xl mx-auto bg-white p-8 rounded-xl shadow-md"
      >
        <h2 className="text-2xl font-bold text-blue-800 text-center">
          Transferencia SINPE
        </h2>

        {/* Cuenta origen */}
        <div>
          <label className="block text-sm font-medium mb-1">
            Cuenta origen
          </label>
          <select
            value={fromAccount}
            onChange={(e) => {
              const acc = accounts.find((a) => a.number === e.target.value);
              setFromAccount(e.target.value);
              if (acc) setCurrency(acc.currency);
            }}
            className="w-full rounded-md px-4 py-3 border-gray-300 shadow-sm"
            required
          >
            {accounts.map((acc) => (
              <option key={acc.id} value={acc.number}>
                {acc.number} ({acc.currency})
              </option>
            ))}
          </select>
          {selectedAccount && (
            <p className="text-sm text-gray-500 mt-1">
              Saldo disponible:{" "}
              {selectedAccount.balance.toLocaleString("es-CR", {
                style: "currency",
                currency: selectedAccount.currency,
              })}
            </p>
          )}
        </div>

        {/* Teléfono */}
        <div>
          <label className="block text-sm font-medium mb-1">
            Número de teléfono
          </label>
          <input
            type="tel"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="Ej: 88888888"
            className="w-full rounded-md px-4 py-3 border-gray-300 shadow-sm"
            required
          />
          {receiverName && (
            <p className="text-sm text-green-600 mt-1">
              Destinatario: {receiverName}
            </p>
          )}
        </div>

        {/* Monto */}
        <div>
          <label className="block text-sm font-medium mb-1">Monto</label>
          <div className="flex gap-2">
            <select
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
              className="rounded-md px-3 py-2 border-gray-300 shadow-sm"
            >
              <option value="CRC">₡</option>
              <option value="USD">$</option>
              <option value="EUR">€</option>
            </select>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="Monto"
              className="flex-1 rounded-md px-4 py-3 border-gray-300 shadow-sm"
              required
              min={0.01}
              step="0.01"
            />
          </div>
          {!isValidAmount && (
            <p className="text-sm text-red-600 mt-1">
              El monto excede el saldo disponible.
            </p>
          )}
        </div>

        {/* Comentario */}
        <div>
          <label className="block text-sm font-medium mb-1">
            Comentario (opcional)
          </label>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Motivo de la transferencia"
            className="w-full rounded-md px-4 py-3 border-gray-300 shadow-sm resize-none"
            rows={3}
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white font-semibold py-3 rounded-md hover:bg-blue-700 transition"
        >
          Continuar
        </button>
      </form>

      {/* Modal de error */}
      <ModalMessage
        isOpen={modalError}
        type="error"
        message="Este número no está registrado en SINPE Móvil."
        onClose={() => setModalError(false)}
      />
    </>
  );
};

export default SinpeTransferForm;
