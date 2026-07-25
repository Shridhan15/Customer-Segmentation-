import React from "react";

export default function PersonaCard({ clusterId, features, centerData }) {
  const getPersonaName = (id) => {
    const names = [
      "The Wealthy Saver",
      "The Active Transactor",
      "The Dormant Account",
    ];
    return names[id] || `Segment ${id + 1}`;
  };

  return (
    <div className="bg-white rounded-xl shadow-md border overflow-hidden">
      <div className="bg-indigo-600 p-4">
        <h4 className="text-white font-bold text-lg">
          {getPersonaName(clusterId)}
        </h4>
        <p className="text-indigo-100 text-xs">Cluster ID: {clusterId}</p>
      </div>

      <div className="p-4 space-y-3">
        <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
          Average Metrics
        </p>

        {features.map((feat, idx) => {
          // FIX: Safe extraction that prevents NaN errors.
          // Handles both Array and Object data structures gracefully.
          const rawValue = Array.isArray(centerData)
            ? centerData[idx]
            : centerData[feat] || 0;
          const displayValue = !isNaN(parseFloat(rawValue))
            ? Number(rawValue).toFixed(2)
            : "0.00";

          return (
            <div
              key={idx}
              className="flex justify-between items-center border-b pb-2"
            >
              <span className="text-sm text-gray-600">
                {feat.replace(/_/g, " ")}
              </span>
              <span className="text-sm font-bold text-gray-800">
                {displayValue}
              </span>
            </div>
          );
        })}

        <div className="mt-4 pt-2">
          <button className="w-full bg-gray-100 text-gray-700 hover:bg-gray-200 py-2 rounded text-sm font-medium transition">
            View Target Strategy
          </button>
        </div>
      </div>
    </div>
  );
}
