import React from "react";
import PersonaCard from "./PersonaCard";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function DashboardView({ data }) {
  if (!data) {
    return (
      <div className="flex items-center justify-center h-full text-gray-400">
        Submit a query to generate insights...
      </div>
    );
  }

  const { agent_reasoning, insights, data_payload } = data;

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">
        Segmentation Insights
      </h2>

      {/* Agent Reasoning Metrics */}
      <div className="flex gap-4 mb-6">
        <div className="bg-white p-4 shadow-sm rounded-lg border w-1/3">
          <p className="text-xs text-gray-500 uppercase">Detected Intent</p>
          <p className="text-lg font-semibold">
            {agent_reasoning?.detected_intent}
          </p>
        </div>
        <div className="bg-white p-4 shadow-sm rounded-lg border w-1/3">
          <p className="text-xs text-gray-500 uppercase">
            Clustering Score (Silhouette)
          </p>
          <p className="text-lg font-semibold">
            {agent_reasoning?.evaluation_metrics}
          </p>
        </div>
      </div>

      {/* The Plain-English Explanation */}
      <div className="bg-blue-50 p-6 rounded-lg border border-blue-100">
        <h3 className="font-semibold text-blue-900 mb-2">Agent Analysis</h3>
        <p className="text-sm text-blue-800 whitespace-pre-line">{insights}</p>
      </div>

      {/* Visualizing Persona Clusters */}
      {data_payload?.cluster_centers && (
        <div className="grid grid-cols-2 gap-4 mt-6">
          {data_payload.cluster_centers.map((center, idx) => (
            <PersonaCard
              key={idx}
              clusterId={idx}
              features={agent_reasoning.features_used}
              centerData={center}
            />
          ))}
        </div>
      )}
    </div>
  );
}
