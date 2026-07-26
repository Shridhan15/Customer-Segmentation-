import React, { useState } from "react";
import { Send, Loader2, ChevronRight, Terminal } from "lucide-react";
import { sendChatQuery } from "../services/api";

const SUGGESTED_PROMPTS = [
  "Segment Customers",
  "Recommend Products",
  "High Value Customers",
  "Loyal Customers",
  "Predict Churn",
];

export default function ChatInterface({ onResponseReceived }) {
  const [query, setQuery] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentThread, setCurrentThread] = useState(null);
  const [pendingClarification, setPendingClarification] = useState(null);

  const handleSend = async (textToSubmit = query) => {
    if (!textToSubmit.trim()) return;

    const userMessage = { role: "user", content: textToSubmit };
    setChatHistory((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const payloadQuery = pendingClarification ? "" : textToSubmit;
      const clarification = pendingClarification ? textToSubmit : null;

      const response = await sendChatQuery(
        payloadQuery,
        currentThread,
        clarification,
      );

      setCurrentThread(response.thread_id);

      if (response.needs_human_input) {
        setChatHistory((prev) => [
          ...prev,
          { role: "system", content: response.clarification_question },
        ]);
        setPendingClarification(true);
      } else {
        // 1. Extract the dynamic response message from the agent state
        const displayMessage =
          response.response_message || "Processing complete.";

        setChatHistory((prev) => [
          ...prev,
          {
            role: "system",
            content: displayMessage,
          },
        ]);

        setPendingClarification(false);

        // 2. Only pass the response to the dashboard if a data payload exists
        if (response.data_payload) {
          console.log("Sending to Dashboard:", response.data_payload);
          onResponseReceived(response);
        }
      }
    } catch (error) {
      setChatHistory((prev) => [
        ...prev,
        { role: "system", content: "Error executing query. Check connection." },
      ]);
    }

    setQuery("");
    setLoading(false);
  };

  return (
    <div className="flex flex-col h-full bg-white">
      <div className="flex-1 overflow-y-auto p-5 space-y-4">
        {chatHistory.length === 0 ? (
          <div className="text-center text-slate-400 mt-10">
            <Terminal size={32} className="mx-auto mb-3 opacity-30" />
            <p className="text-sm font-medium">Ready for data queries</p>
          </div>
        ) : (
          chatHistory.map((msg, idx) => (
            <div
              key={idx}
              className={`p-3 rounded-xl text-[13.5px] max-w-[90%] shadow-sm ${
                msg.role === "user"
                  ? "bg-slate-800 text-white self-end ml-auto"
                  : "bg-slate-50 text-slate-700 self-start border border-slate-200"
              }`}
            >
              <p className="leading-relaxed">{msg.content}</p>
            </div>
          ))
        )}
        {loading && (
          <div className="flex justify-center p-4">
            <Loader2 className="animate-spin text-indigo-500" size={24} />
          </div>
        )}
      </div>

      <div className="p-4 bg-white border-t border-slate-200 space-y-4 z-10">
        <div className="flex flex-wrap gap-2.5">
          {SUGGESTED_PROMPTS.map((prompt, idx) => (
            <button
              key={idx}
              onClick={() => {
                setQuery(prompt);
                handleSend(prompt);
              }}
              className="text-[12px] font-semibold bg-white border border-slate-200 text-slate-600 px-3 py-1.5 rounded-full hover:border-indigo-400 hover:text-indigo-700 transition-colors flex items-center gap-1 shadow-sm whitespace-nowrap"
            >
              {prompt} <ChevronRight size={12} className="opacity-70" />
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2 bg-white border-2 border-slate-200 rounded-xl p-1.5 shadow-sm focus-within:border-indigo-500 transition-all">
          <input
            type="text"
            className="flex-1 p-2 outline-none text-[14px] text-slate-800 bg-transparent placeholder-slate-400 font-medium"
            placeholder={
              pendingClarification
                ? "Provide clarification..."
                : "Enter query parameters..."
            }
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend(query)}
          />
          <button
            onClick={() => handleSend(query)}
            disabled={loading || !query.trim()}
            className="bg-indigo-600 text-white p-2.5 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
