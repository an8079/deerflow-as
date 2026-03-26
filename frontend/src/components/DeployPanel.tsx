import { useState } from 'react';
import type { DeploymentTarget } from '../types';
import { cn, statusColor, formatDate } from '../lib/utils';
import { Rocket, ExternalLink, RefreshCw, CheckCircle2, XCircle, Loader2, Zap } from 'lucide-react';

interface Props {
  deployments: DeploymentTarget[];
  onDeploy: (name: string) => Promise<void>;
}

export function DeployPanel({ deployments, onDeploy }: Props) {
  const [deploying, setDeploying] = useState<string | null>(null);

  async function handleDeploy(name: string) {
    setDeploying(name);
    try {
      await onDeploy(name);
    } finally {
      setDeploying(null);
    }
  }

  function statusIcon(status: DeploymentTarget['status']) {
    if (status === 'deploying' || deploying) return <Loader2 className="w-4 h-4 animate-spin text-blue-400" />;
    if (status === 'success') return <CheckCircle2 className="w-4 h-4 text-green-400" />;
    if (status === 'failed') return <XCircle className="w-4 h-4 text-red-400" />;
    return <div className="w-4 h-4" />;
  }

  return (
    <div className="bg-[#1e293b] rounded-xl border border-[#334155] overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-[#334155]">
        <div className="flex items-center gap-2">
          <Rocket className="w-4 h-4 text-indigo-400" />
          <span className="text-sm font-semibold">一键部署</span>
        </div>
        <button
          onClick={() => deployments.forEach(d => d.status !== 'deploying' && handleDeploy(d.name))}
          className="flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium px-3 py-1.5 rounded-lg transition-colors"
        >
          <Zap className="w-3 h-3" />
          全部部署
        </button>
      </div>
      <div className="divide-y divide-[#0f172a]">
        {deployments.map(d => (
          <div key={d.name} className="flex items-center gap-3 px-4 py-3 hover:bg-[#0f172a]/30 transition-colors">
            <div className="flex-shrink-0">{statusIcon(d.status)}</div>
            <div className="flex-1 min-w-0">
              <div className="text-sm font-medium">{d.name}</div>
              <div className="flex items-center gap-2 mt-0.5">
                <div className={cn('w-1.5 h-1.5 rounded-full', statusColor(d.status))} />
                <span className="text-xs text-[#94a3b8]">
                  {d.status === 'deploying' ? '部署中...' :
                   d.status === 'success' ? '已部署' :
                   d.status === 'failed' ? '失败' : '空闲'}
                </span>
                {d.lastDeployed && (
                  <span className="text-xs text-[#64748b]">· {formatDate(d.lastDeployed)}</span>
                )}
              </div>
            </div>
            <div className="flex items-center gap-2 flex-shrink-0">
              {d.url && (
                <a href={d.url} target="_blank" rel="noopener noreferrer"
                  className="text-[#94a3b8] hover:text-indigo-400 transition-colors">
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
              {d.status !== 'deploying' && (
                <button
                  onClick={() => handleDeploy(d.name)}
                  disabled={deploying !== null}
                  className="flex items-center gap-1 text-xs bg-[#0f172a] hover:bg-[#334155] text-[#94a3b8] hover:text-white px-2 py-1 rounded-lg transition-colors"
                >
                  <RefreshCw className="w-3 h-3" />
                  部署
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
