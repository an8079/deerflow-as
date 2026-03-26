import type { Task } from '../types';
import { cn, statusColor, taskStatusLabel, progressColor } from '../lib/utils';

const COLUMNS: { key: Task['status']; label: string; color: string }[] = [
  { key: 'queued', label: '排队中', color: 'border-amber-400/40' },
  { key: 'pending', label: '待处理', color: 'border-gray-500/40' },
  { key: 'running', label: '进行中', color: 'border-blue-500/40' },
  { key: 'completed', label: '已完成', color: 'border-green-500/40' },
  { key: 'failed', label: '失败', color: 'border-red-500/40' },
];

interface Props {
  tasks: Task[];
  onSelect: (task: Task) => void;
  selectedId?: string;
}

export function TaskBoard({ tasks, onSelect, selectedId }: Props) {
  return (
    <div className="flex gap-3 h-full overflow-x-auto pb-1">
      {COLUMNS.map(col => {
        const colTasks = tasks.filter(t => t.status === col.key);
        return (
          <div key={col.key} className={cn('flex-shrink-0 w-52 flex flex-col rounded-xl border-t-2', col.color, 'bg-[#0f172a]/50')}>
            <div className="flex items-center justify-between px-3 py-2.5 border-b border-[#1e293b]">
              <span className="text-xs font-semibold text-[#94a3b8]">{col.label}</span>
              <span className="text-xs bg-[#1e293b] text-[#94a3b8] px-1.5 py-0.5 rounded-full">{colTasks.length}</span>
            </div>
            <div className="flex-1 overflow-y-auto p-2 flex flex-col gap-2">
              {colTasks.map(task => (
                <div
                  key={task.id}
                  onClick={() => onSelect(task)}
                  className={cn(
                    'bg-[#1e293b] rounded-lg p-3 border cursor-pointer transition-all hover:scale-[1.02]',
                    selectedId === task.id ? 'border-indigo-500 shadow-lg shadow-indigo-500/10' : 'border-[#334155] hover:border-[#475569]'
                  )}
                >
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <span className="text-sm font-medium leading-tight">{task.title}</span>
                    {task.assignee && (
                      <span className="text-base flex-shrink-0">{task.assignee.avatar}</span>
                    )}
                  </div>
                  {task.tags && task.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1 mb-2">
                      {task.tags.map(tag => (
                        <span key={tag} className="text-[9px] bg-[#0f172a] text-[#94a3b8] px-1.5 py-0.5 rounded">{tag}</span>
                      ))}
                    </div>
                  )}
                  <div className="flex items-center gap-2">
                    <div className="flex-1 h-1.5 bg-[#0f172a] rounded-full overflow-hidden">
                      <div className={cn('h-full rounded-full transition-all', progressColor(task.progress))} style={{ width: `${task.progress}%` }} />
                    </div>
                    <span className="text-[10px] text-[#94a3b8]">{task.progress}%</span>
                  </div>
                  <div className="flex items-center gap-1.5 mt-1.5">
                    <div className={cn('w-1.5 h-1.5 rounded-full', statusColor(task.status))} />
                    <span className="text-[10px] text-[#94a3b8]">{taskStatusLabel(task.status)}</span>
                  </div>
                </div>
              ))}
              {colTasks.length === 0 && (
                <div className="text-center text-[#334155] text-xs py-6">无任务</div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
