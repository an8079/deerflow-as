import type { Project } from '../types';
import { cn } from '../lib/utils';

interface Props {
  projects: Project[];
  selectedId: string;
  onSelect: (id: string) => void;
}

export function ProjectSidebar({ projects, selectedId, onSelect }: Props) {
  return (
    <div className="w-56 flex-shrink-0 flex flex-col gap-1">
      <div className="text-xs font-semibold text-[#94a3b8] uppercase tracking-wider px-2 mb-1">项目列表</div>
      {projects.map(p => (
        <button
          key={p.id}
          onClick={() => onSelect(p.id)}
          className={cn(
            'w-full text-left px-3 py-2.5 rounded-lg border transition-all group',
            selectedId === p.id
              ? 'bg-[#1e293b] border-indigo-500/50'
              : 'bg-transparent border-transparent hover:bg-[#1e293b]/60 hover:border-[#334155]'
          )}
        >
          <div className="flex items-center gap-2 mb-1">
            <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: p.color }} />
            <span className={cn('text-sm font-medium truncate', selectedId === p.id ? 'text-white' : 'text-[#cbd5e1]')}>{p.name}</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="flex-1 h-1 bg-[#0f172a] rounded-full overflow-hidden">
              <div className="h-full rounded-full transition-all" style={{ width: `${p.progress}%`, backgroundColor: p.color }} />
            </div>
            <span className="text-[10px] text-[#94a3b8]">{p.progress}%</span>
          </div>
          <div className="flex items-center gap-3 mt-1">
            <span className="text-[10px] text-[#94a3b8]">{p.completedTasks}/{p.taskCount} 任务</span>
            <span className={cn('text-[10px] px-1.5 py-0.5 rounded-full',
              p.status === 'active' ? 'bg-green-500/20 text-green-400' :
              p.status === 'paused' ? 'bg-amber-500/20 text-amber-400' :
              'bg-blue-500/20 text-blue-400'
            )}>
              {p.status === 'active' ? '活跃' : p.status === 'paused' ? '暂停' : '完成'}
            </span>
          </div>
        </button>
      ))}
    </div>
  );
}
