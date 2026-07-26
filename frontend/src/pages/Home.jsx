import React, { useState } from "react";
import ChatInterface from "../components/ChatInterface";
import DashboardView from "../components/DashboardView";
import { LayoutDashboard, Search } from "lucide-react";

export default function Home() {
  const [agentResponse, setAgentResponse] = useState(null);

  return (
    <div className="flex flex-col h-screen bg-slate-50 font-sans text-slate-800">
      <header className="h-16 bg-white border-b border-slate-200 flex items-center px-6 shadow-sm shrink-0 justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg text-white">
            <LayoutDashboard size={20} />
          </div>
          <h1 className="text-xl font-bold tracking-tight text-slate-900">
            Customer Intelligence Analytics
          </h1>
        </div>
        <div className="flex items-center gap-4 text-sm font-medium text-slate-500">
          <span>Enterprise Workspace</span>
          <div className="w-8 h-8 rounded-full bg-slate-200 border border-slate-300 flex items-center justify-center text-slate-600 font-bold">
            WS
          </div>
        </div>
      </header>

      <div className="flex-1 flex overflow-hidden">
        <aside className="w-[400px] bg-white border-r border-slate-200 shadow-sm flex flex-col z-10 shrink-0">
          <div className="p-5 border-b border-slate-100 flex items-center gap-2 text-slate-800 font-semibold">
            <Search size={18} className="text-slate-400" />
            Query Console
          </div>
          <div className="flex-1 overflow-hidden">
            <ChatInterface
              onResponseReceived={(response) => {
                console.log("Home received:", response);
                setAgentResponse(response);
              }}
            />
          </div>
        </aside>

        <main className="flex-1 overflow-y-auto bg-slate-50/50 p-8">
          <DashboardView data={agentResponse} />
        </main>
      </div>
    </div>
  );
}
