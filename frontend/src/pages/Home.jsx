
import React, { useState } from "react";
import ChatInterface from "../components/ChatInterface";
import DashboardView from "../components/DashboardView";

export default function Home() {
  const [agentResponse, setAgentResponse] = useState(null);

  return (
    <div className="flex h-screen w-full">
      <div className="w-1/3 border-r bg-white flex flex-col shadow-lg">
        <div className="p-4 bg-blue-900 text-white font-bold text-xl">
          Retail Banking Agent
        </div>
        <ChatInterface onResponseReceived={setAgentResponse} />
      </div>

      <div className="w-2/3 p-6 overflow-y-auto">
        <DashboardView data={agentResponse} />
      </div>
    </div>
  );
}
