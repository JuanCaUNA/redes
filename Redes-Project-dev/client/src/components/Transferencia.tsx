import React, { useState } from "react";
import TransferForm from "./TransferForm";
import type { TransferData } from "./TransferForm";
import TransferSummary from "./TransferSummary";
import TransferProcessing from "./TransferProcessing";

const Transferencia: React.FC = () => {
  const [step, setStep] = useState<"form" | "summary" | "processing">("form");
  const [transferData, setTransferData] = useState<TransferData | null>(null);

  const handleFormSubmit = (data: TransferData) => {
    setTransferData(data);
    setStep("summary");
  };

  const handleConfirm = () => {
    setStep("processing");
  };

  const handleCancel = () => {
    setTransferData(null);
    setStep("form");
  };

  const handleFinish = () => {
    setTransferData(null);
    setStep("form");
  };

  return (
    <div className="p-6">
      {step === "form" && (
        <TransferForm
          userId="default"
          onSubmit={handleFormSubmit}
          subscribedAccounts={[]}
        />
      )}
      {step === "summary" && transferData && (
        <TransferSummary
          data={transferData}
          onConfirm={handleConfirm}
          onCancel={handleCancel}
        />
      )}
      {step === "processing" && <TransferProcessing onFinish={handleFinish} />}
    </div>
  );
};

export default Transferencia;
