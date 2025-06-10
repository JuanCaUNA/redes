import React from "react";

interface Account {
  id: string;
  name: string;
  number: string;
  balance: number;
}

interface Props {
  accounts: Account[];
}

const AccountList: React.FC<Props> = ({ accounts }) => {
  return (
    <div>
      <h2 className="text-xl font-bold text-blue-700 mb-4">
        Cuentas Registradas
      </h2>
      <ul className="space-y-2">
        {accounts.map((acc) => (
          <li
            key={acc.id}
            className="p-4 border border-gray-200 rounded-md shadow-sm bg-white"
          >
            <p>
              <strong>Nombre:</strong> {acc.name}
            </p>
            <p>
              <strong>Número:</strong> {acc.number}
            </p>
            <p>
              <strong>Saldo:</strong> ₡{acc.balance.toLocaleString()}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AccountList;
