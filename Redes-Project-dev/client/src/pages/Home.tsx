import React from "react";

const Home: React.FC = () => {
  return (
    <div className="max-w-2xl mx-auto mt-20 text-center">
      <h1 className="text-4xl font-bold text-blue-800 mb-4">
        Bienvenido a NetBank
      </h1>
      <p className="text-gray-700 text-lg mb-6">
        Tu plataforma confiable para gestionar cuentas, realizar transferencias
        y más.
      </p>
      <p className="text-gray-600">
        Utiliza el menú lateral para comenzar. Puedes crear cuentas bancarias,
        consultar información o realizar operaciones de forma segura y sencilla.
      </p>
    </div>
  );
};

export default Home;
