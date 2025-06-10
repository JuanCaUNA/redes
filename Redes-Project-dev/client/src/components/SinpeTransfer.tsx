import React, { useState, useEffect } from "react";
import SinpeTransferForm from "./SinpeTransferForm";
import SinpeTransferSummary from "./SinpeTransferSummary";
import SinpeTransferProcessing from "./SinpeTransferProcessing";

interface SinpeTransferData {
  fromAccount: string;
  phone: string;
  amount: number;
  currency: string;
  comment?: string;
}

const SinpeTransfer: React.FC = () => {
  const [step, setStep] = useState<"form" | "summary" | "processing">("form");
  const [transferData, setTransferData] = useState<SinpeTransferData | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem("pendingSinpeTransfer");
    if (saved) {
      setTransferData(JSON.parse(saved));
      setStep("summary");
    }
  }, []);

  const handleFormSubmit = (data: SinpeTransferData) => {
    setTransferData(data);
    localStorage.setItem("pendingSinpeTransfer", JSON.stringify(data));
    setStep("summary");
  };

  const handleConfirm = () => {
    setStep("processing");
  };

  const handleCancel = () => {
    localStorage.removeItem("pendingSinpeTransfer");
    setTransferData(null);
    setStep("form");
  };

  const handleFinish = () => {
    localStorage.removeItem("pendingSinpeTransfer");
    setTransferData(null);
    setStep("form");
  };

  return (
    <div className="p-6">
      {step === "form" && (
        <SinpeTransferForm onContinue={handleFormSubmit} />
      )}
      {step === "summary" && transferData && (
        <SinpeTransferSummary
          data={transferData}
          onConfirm={handleConfirm}
          onCancel={handleCancel}
        />
      )}
      {step === "processing" && (
        <SinpeTransferProcessing onFinish={handleFinish} />
      )}
    </div>
  );
};

export default SinpeTransfer;
