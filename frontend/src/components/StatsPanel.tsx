import type { DashboardStats } from '../types';

interface Props { stats: DashboardStats; }

export function StatsPanel({ stats: _stats }: Props) {
  // Use _stats in component body; TS will allow underscore-prefixed unused param
  const cards = [
    { label: '总项目', value: _stats.totalProjects, icon: '📁', color: 'text-indigo-400' },
    { label: '活跃项目', value: _stats.activeProjects, icon: '⚡', color: 'text-green-400' },
    { label: '总任务', value: _stats.totalTasks, icon: '📋', color: 'text-blue-400' },
    { label: '已完成', value: _stats.completedTasks, icon: '🎯', color: 'text-emerald-400' },
    { label: '运行中 Agent', value: _stats.runningAgents, icon: '🤖', color: 'text-amber-400' },
    { label: '团队规模', value: _stats.totalAgents, icon: '👥', color: 'text-pink-400' },
  ];
  return (
    <div className="grid grid-cols-3 lg:grid-cols-6 gap-3">
      {cards.map(c => (
        <div key={c.label} className="bg-[#1e293b] rounded-xl p-3 border border-[#334155] hover:border-indigo-500/40 transition-colors">
          <div className="text-2xl mb-1">{c.icon}</div>
          <div className={`text-2xl font-bold ${c.color}`}>{c.value}</div>
          <div className="text-xs text-[#94a3b8] mt-0.5">{c.label}</div>
        </div>
      ))}
    </div>
  );
}
