import React from "react";
import { Users, Target, ChevronRight } from "lucide-react";

export default function PersonaCard({ 
  clusterId, 
  name,
  features, 
  centerData, 
  population,
  totalPopulation,
  color, 
  onClick,
  isSelected
}) {
  
  const popPercentage = (totalPopulation > 0 && population > 0) ? (population / totalPopulation) * 100 : 0;
  
  const formatNumber = (num) => {
    if (typeof num !== 'number' || isNaN(num)) return "0";
    if (num > 1000) return (num / 1000).toFixed(1) + 'k';
    return num.toLocaleString(undefined, { maximumFractionDigits: 1 });
  };

  return (
    <div 
      onClick={onClick}
      className={`relative bg-white rounded-2xl border-2 transition-all cursor-pointer group flex flex-col h-full overflow-hidden ${
        isSelected ? 'shadow-md scale-[1.02]' : 'shadow-sm hover:shadow-lg border-slate-100 hover:border-slate-300'
      }`}
      style={isSelected ? { borderColor: color } : {}}
    >
      <div className="h-2 w-full" style={{ backgroundColor: color }} />
      
      <div className="p-6 flex-1 flex flex-col">
        <div className="flex justify-between items-start mb-6">
          <div className="min-w-0 pr-3 flex-1">
            <h4 className="font-black text-[18px] text-slate-800 break-words leading-tight" title={name}>{name}</h4>
            <div className="flex items-center gap-1.5 mt-2 text-slate-500 text-[13px] font-bold">
              <Users size={16} />
              <span>{population > 0 ? population.toLocaleString() : "Unknown"} users</span>
            </div>
          </div>
          <div 
            className="w-11 h-11 rounded-xl flex items-center justify-center text-white shadow-sm shrink-0"
            style={{ backgroundColor: color }}
          >
            <Target size={20} />
          </div>
        </div>

        <div className="mb-8">
          <div className="flex justify-between text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2.5">
            <span>Population Share</span>
            <span className="text-slate-600">{popPercentage.toFixed(1)}%</span>
          </div>
          <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
            <div 
              className="h-2.5 rounded-full transition-all duration-1000" 
              style={{ width: `${popPercentage}%`, backgroundColor: color }} 
            />
          </div>
        </div>

        <div className="space-y-4 flex-1">
          {features.slice(0, 4).map((feat, idx) => {
            const val = Number(centerData[feat]) || 0;
            
            return (
              <div key={idx} className="flex justify-between items-center text-[13.5px] border-b border-slate-50 pb-2">
                <span className="font-semibold text-slate-500 capitalize break-words pr-2 flex-1">
                  {feat.replace(/_/g, ' ')}
                </span>
                <span className="font-black text-slate-800 bg-slate-100 px-2 py-0.5 rounded-md">
                  {formatNumber(val)}
                </span>
              </div>
            );
          })}
        </div>
        
        <div className={`mt-6 pt-5 border-t border-slate-100 flex items-center justify-between transition-colors ${isSelected ? 'text-slate-800' : 'text-slate-400 group-hover:text-slate-700'}`}>
          <span className="text-[13px] font-black uppercase tracking-wide">View Strategy</span>
          <ChevronRight size={18} />
        </div>
      </div>
    </div>
  );
}