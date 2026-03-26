import type { Task } from '../types';
import { cn, statusColor, taskStatusLabel, progressColor, formatDate } from '../lib/utils';
import { X, Bot, ChevronRight } from 'lucide-react';

interface Props { task: Task | null; onClose: () => void; }

export function TaskDetailPanel({ task, onClose }: Props) {
  if (!task) {
    return (
      <div className="w-80 flex-shrink-0 bg-[#1e293b] rounded-xl border border-[#334155] flex items-center justify-center">
        <div className="text-center text-[#334155]">
          <div className="text-3xl mb-2">📋</div>
          <div className="text-sm">选择任务查看详情</div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-80 flex-shrink-0 bg-[#1e293b] rounded-xl border border-[#334155] flex flex-col overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-[#334155]">
        <div className="flex items-center gap-2">
          <Bot className="w-4 h-4 text-indigo-400" />
          <span className="text-sm font-semibold">任务详情</span>
        </div>
        <button onClick={onClose} className="text-[#94a3b8] hover:text-white transition-colors">
          <X className="w-4 h-4" />
        </button>
      </div>
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4">
        <div>
          <h3 className="text-base font-semibold mb-2">{task.title}</h3>
          <div className="flex items-center gap-2">
            <div className={cn('w-2 h-2 rounded-full', statusColor(task.status))} />
            <span className="text-sm text-[#94a3b8]">{taskStatusLabel(task.status)}</span>
          </div>
        </div>
        <div>
          <div className="text-xs text-[#94a3b8] mb-1">描述</div>
          <div className="text-sm bg-[#0f172a] rounded-lg p-2.5 leading-relaxed">{task.description}</div>
        </div>
        {task.assignee && (
          <div>
            <div className="text-xs text-[#94a3b8] mb-1">执行 Agent</div>
            <div className="flex items-center gap-2 bg-[#0f172a] rounded-lg p-2.5">
              <span className="text-xl">{task.assignee.avatar}</span>
              <div>
                <div className="text-sm font-medium">{task.assignee.name}</div>
                <div className="text-xs text-[#94a3b8]">{task.assignee.role}</div>
              </div>
              <div className={cn('ml-auto w-2 h-2 rounded-full', statusColor(task.assignee.status))} />
            </div>
          </div>
        )}
        <div>
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-xs text-[#94a3b8]">进度</span>
            <span className="text-xs font-medium">{task.progress}%</span>
          </div>
          <div className="h-2.5 bg-[#0f172a] rounded-full overflow-hidden">
            <div className={cn('h-full rounded-full transition-all', progressColor(task.progress))} style={{ width: `${task.progress}%` }} />
          </div>
        </div>
        {task.tags && task.tags.length > 0 && (
          <div>
            <div className="text-xs text-[#94a3b8] mb-1">标签</div>
            <div className="flex flex-wrap gap-1.5">
              {task.tags.map(tag => (
                <span key={tag} className="text-xs bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded-full border border-indigo-500/30">{tag}</span>
              ))}
            </div>
          </div>
        )}
        {task.output && (
          <div>
            <div className="text-xs text-[#94a3b8] mb-1">输出结果</div>
            <div className="bg-[#0f172a] rounded-lg p-3 text-sm text-emerald-300/80 leading-relaxed border border-emerald-500/10">
              <ChevronRight className="w-3 h-3 inline mr-1" />
              {task.output}
            </div>
          </div>
        )}
        {task.logs && task.logs.length > 0 && (
          <div>
            <div className="text-xs text-[#94a3b8] mb-1">日志</div>
            <div className="bg-[#0f172a] rounded-lg p-2.5 font-mono text-xs space-y-1 max-h-32 overflow-y-auto">
              {task.logs.map((log, i) => <div key={i} className="text-[#94a3b8]">$ {log}</div>)}
            </div>
          </div>
        )}
        <div className="border-t border-[#334155] pt-3 mt-auto space-y-1.5">
          <div className="flex justify-between text-xs text-[#64748b]"><span>创建时间</span><span>{formatDate(task.createdAt)}</span></div>
          <div className="flex justify-between text-xs text-[#64748b]"><span>更新时间</span><span>{formatDate(task.updatedAt)}</span></div>
          <div className="flex justify-between text-xs text-[#64748b]"><span>任务 ID</span><span className="font-mono">{task.id}</span></div>
        </div>
      </div>
    </div>
  );
}
