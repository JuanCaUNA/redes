import React, { useState } from "react";
import { Sidebar } from "./Sidebar";
import Home from "../pages/Home";
import CreateAccountForm from "./AccountForm";
import ViewAccounts from "../pages/ViewAccounts";
import SubscribeAccount from "./SubscribeAccount";
import Transferencia from "./Transferencia";
import CreateUser from "./CreateUser";
import PhoneLink from "./PhoneLink";
import SinpeTransfer from "./SinpeTransfer";

export interface Account {
  id: string;
  name: string;
  number: string;
  balance: number;
}

export const Layout: React.FC = () => {
  const [activeTabId, setActiveTabId] = useState("home");
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const username = user?.name || "";

  const sections = [
    {
      id: "home",
      label: "Inicio",
      title: "Bienvenida a NovaFin",
      content: <Home />,
    },
    {
      id: "ver-cuentas",
      label: "Ver Cuentas",
      title: "Cuentas Registradas",
      content: <ViewAccounts />,
    },
    {
      id: "suscripcion",
      label: "Suscripción",
      title: "Suscripción a Cuentas",
      content: <SubscribeAccount />,
    },
    {
      id: "transferencia",
      label: "Transferencias",
      title: "Realizar transferencia",
      content: <Transferencia />,
    },
    {
      id : "Suscripcion a Numero",
      label : " Suscripción a Sinpe Movil",
      title: "Asociar cuenta a número de teléfono",
      content : <PhoneLink />,
    },
    {
      id : "Sinpe Movil",
      label : "Sinpe Movil",
      title: "Realizar transferencia a través de Sinpe Móvil",
      content : <SinpeTransfer/>,
    }
  ];

  // Agrega secciones solo si el usuario es admin
  if (username.toLowerCase() === "admin") {
    sections.splice(1, 0, {
      id: "crear-cuenta",
      label: "Crear Cuenta",
      title: "Formulario de nueva cuenta",
      content: <CreateAccountForm />,
    });
    sections.push({
      id: "Creacion de Usuario",
      label: "Crear Usuario",
      title: "Crear un nuevo usuario",
      content: <CreateUser />,
    });
  }

  const activeContent = sections.find((s) => s.id === activeTabId)?.content;

  return (
    <div className="flex min-h-screen">
      <Sidebar
        sections={sections.map((s) => ({
          ...s,
          onClick: () => setActiveTabId(s.id),
          isActive: s.id === activeTabId,
        }))}
      />
      <main className="ml-[300px] flex-1 p-6 overflow-auto">
        {activeContent}
      </main>
    </div>
  );
};
