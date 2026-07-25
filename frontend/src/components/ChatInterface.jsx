import React, { useState } from "react";
import { sendChatQuery } from "../services/api";
import { Send, Loader2 } from "lucide-react";

export default function ChatInterface({ onResponseReceived }) {
  const [query, setQuery] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentThread, setCurrentThread] = useState(null);
  const [pendingClarification, setPendingClarification] = useState(null);

  const handleSend = async () => {
    if (!query.trim()) return;

    const userMessage = { role: "user", content: query };
    setChatHistory((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const payloadQuery = pendingClarification ? "" : query;
      const clarification = pendingClarification ? query : null;

      const response = await sendChatQuery(
        payloadQuery,
        currentThread,
        clarification,
      );

      setCurrentThread(response.thread_id);

      if (response.needs_human_input) {
        setChatHistory((prev) => [
          ...prev,
          { role: "agent", content: response.clarification_question },
        ]);
        setPendingClarification(true);
      } else {
        setChatHistory((prev) => [
          ...prev,
          {
            role: "agent",
            content: "Task complete. I have generated the insights.",
          },
        ]);
        setPendingClarification(false);
        onResponseReceived(response);  
      }
    } catch (error) {
      setChatHistory((prev) => [
        ...prev,
        { role: "agent", content: "Error connecting to the AI agent." },
      ]);
    }

    setQuery("");
    setLoading(false);
  };

  return (
    <div className="flex flex-col h-full bg-white">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {chatHistory.map((msg, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-lg max-w-[85%] ${msg.role === "user" ? "bg-blue-100 self-end ml-auto" : "bg-gray-100 self-start"}`}
          >
            <p className="text-sm text-gray-800">{msg.content}</p>
          </div>
        ))}
        {loading && <Loader2 className="animate-spin text-blue-500 mx-auto" />}
      </div>

      <div className="p-4 border-t flex items-center gap-2">
        <input
          type="text"
          className="flex-1 border rounded-md p-2 outline-none focus:ring-2 focus:ring-blue-400"
          placeholder={
            pendingClarification
              ? "Answer the agent..."
              : "Ask the agent to segment customers..."
          }
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button
          onClick={handleSend}
          className="bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700"
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
}
