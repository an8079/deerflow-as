import { useState } from 'react';
import type { Agent } from '../types';
import { cn, statusColor } from '../lib/utils';

const ROLE_COLORS: Record<string, string> = {
  'CEO': 'ring-amber-400',
  'Architect': 'ring-purple-400',
  'Frontend Dev': 'ring-blue-400',
  'Backend Dev': 'ring-cyan-400',
  'QA Engineer': 'ring-green-400',
  'DevOps': 'ring-orange-400',
  'Product Manager': 'ring-pink-400',
  'Designer': 'ring-rose-400',
  'Data Analyst': 'ring-teal-400',
  'Security Engineer': 'ring-red-400',
};

interface Props { agents: Agent[]; }

export function TeamView({ agents }: Props) {
  const [selected, setSelected] = useState<Agent | null>(null);

  return (
    <div className="flex gap-4 h-full">
      {/* Grid */}
      <div className="flex-1 grid grid-cols-5 gap-3 content-start overflow-y-auto pr-1">
        {agents.map(agent => (
          <div
            key={agent.id}
            onClick={() => setSelected(selected?.id === agent.id ? null : agent)}
            className={cn(
              'flex flex-col items-center gap-1.5 p-3 rounded-xl border transition-all cursor-pointer',
              'hover:scale-105',
              selected?.id === agent.id ? 'bg-[#1e293b] border-indigo-500' : 'bg-[#1e293b]/50 border-[#334155] hover:border-[#475569]'
            )}
          >
            <div className="relative">
              <div className={cn('w-12 h-12 rounded-full bg-[#0f172a] flex items-center justify-center text-2xl ring-2', ROLE_COLORS[agent.role] ?? 'ring-gray-500')}>
                {agent.avatar}
              </div>
              <div className={cn('absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 rounded-full border-2 border-[#0f172a]', agent.status)} />
            </div>
            <div className="text-xs font-medium text-center leading-tight">{agent.name}</div>
            <div className="text-[10px] text-[#94a3b8] text-center leading-tight">{agent.role}</div>
          </div>
        ))}
      </div>

      {/* Detail panel */}
      {selected && (
        <div className="w-64 flex-shrink-0 bg-[#1e293b] rounded-xl border border-[#334155] p-4 flex flex-col gap-3 overflow-y-auto">
          <div className="flex items-center gap-3">
            <div className="text-4xl">{selected.avatar}</div>
            <div>
              <div className="font-semibold">{selected.name}</div>
              <div className="text-sm text-[#94a3b8]">{selected.role}</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className={cn('w-2 h-2 rounded-full', statusColor(selected.status))} />
            <span className="text-sm capitalize">
              {selected.status === 'online' ? '在线' : selected.status === 'busy' ? '忙碌' : '离线'}
            </span>
          </div>
          <div>
            <div className="text-xs text-[#94a3b8] mb-1">当前任务</div>
            <div className="text-sm bg-[#0f172a] rounded-lg p-2">{selected.currentTask ?? '暂无'}</div>
          </div>
          <div>
            <div className="text-xs text-[#94a3b8] mb-1">最后活跃</div>
            <div className="text-xs">{new Date(selected.lastActive).toLocaleString('zh-CN')}</div>
          </div>
        </div>
      )}
    </div>
  );
}
