import React, { useEffect, useState } from "react";

interface Props {
  onFinish: () => void;
}

const SinpeTransferProcessing: React.FC<Props> = ({ onFinish }) => {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
      setTimeout(onFinish, 2000);
    }, 2000);

    return () => clearTimeout(timer);
  }, [onFinish]);

  return (
    <div className="h-full flex items-center justify-center">
      <div className="bg-white p-10 rounded-xl shadow-lg text-center max-w-sm">
        {isLoading ? (
          <>
            <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
            <p className="text-lg text-blue-700 font-medium">
              Procesando transferencia SINPE...
            </p>
          </>
        ) : (
          <>
            <div className="text-5xl text-green-500 mb-4">✅</div>
            <p className="text-lg font-semibold text-green-700">
              Transferencia SINPE realizada con éxito
            </p>
          </>
        )}
      </div>
    </div>
  );
};

export default SinpeTransferProcessing;
