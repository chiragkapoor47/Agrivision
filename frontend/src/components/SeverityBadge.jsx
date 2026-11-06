import React from 'react';
import { ShieldCheck, AlertCircle, AlertTriangle, AlertOctagon, HelpCircle } from 'lucide-react';

export default function SeverityBadge({ level, percentage, showIcon = true, size = 'md' }) {
  const lvl = (level || '').toLowerCase();

  let bg = 'bg-emerald-100 text-emerald-800 border-emerald-300';
  let Icon = ShieldCheck;
  let label = level || 'Healthy';

  if (lvl.includes('severe')) {
    bg = 'bg-red-100 text-red-800 border-red-300 animate-pulse';
    Icon = AlertOctagon;
  } else if (lvl.includes('moderate')) {
    bg = 'bg-amber-100 text-amber-800 border-amber-300';
    Icon = AlertTriangle;
  } else if (lvl.includes('low')) {
    bg = 'bg-lime-100 text-lime-800 border-lime-300';
    Icon = AlertCircle;
  } else if (lvl.includes('uncertain')) {
    bg = 'bg-slate-100 text-slate-800 border-slate-300';
    Icon = HelpCircle;
  }

  const sizeClasses = size === 'sm' ? 'px-2 py-0.5 text-xs' : (size === 'lg' ? 'px-4 py-1.5 text-base font-semibold' : 'px-3 py-1 text-sm font-medium');
  const iconSizes = size === 'sm' ? 'w-3 h-3' : (size === 'lg' ? 'w-5 h-5' : 'w-4 h-4');

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full border ${bg} ${sizeClasses} shadow-2xs`}>
      {showIcon && <Icon className={iconSizes} />}
      <span>{label}</span>
      {percentage !== undefined && percentage !== null && percentage > 0 && (
        <span className="font-bold opacity-90">({percentage}%)</span>
      )}
    </span>
  );
}
