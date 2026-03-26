import { useState } from 'react';
import type { Task } from './types';
import { StatsPanel } from './components/StatsPanel';
import { ProjectSidebar } from './components/ProjectSidebar';
import { TaskBoard } from './components/TaskBoard';
import { TaskDetailPanel } from './components/TaskDetailPanel';
import { TeamView } from './components/TeamView';
import { DeployPanel } from './components/DeployPanel';
import { getProjects, getStats, getDeployments, triggerDeploy } from './api';
import { Layers, Users, BarChart3, Rocket, Plus, ChevronDown, GitBranch } from 'lucide-react';

const projects = getProjects();
const stats = getStats();
const deployments = getDeployments();

type View = 'projects' | 'team' | 'analytics' | 'deploy';

export default function App() {
  const [selectedProjectId, setSelectedProjectId] = useState(projects[0].id);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [view, setView] = useState<View>('projects');
  const [notification, setNotification] = useState<string | null>(null);

  const selectedProject = projects.find(p => p.id === selectedProjectId) ?? projects[0];

  function notify(msg: string) {
    setNotification(msg);
    setTimeout(() => setNotification(null), 3000);
  }

  const navItems = [
    { key: 'projects' as View, label: '项目视图', icon: Layers },
    { key: 'team' as View, label: '团队', icon: Users },
    { key: 'analytics' as View, label: '统计', icon: BarChart3 },
    { key: 'deploy' as View, label: '部署', icon: Rocket },
  ];

  return (
    <div className="h-screen flex flex-col bg-[#0f172a] text-white overflow-hidden">
      {notification && (
        <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 bg-indigo-600 text-white text-sm px-4 py-2 rounded-lg shadow-lg animate-bounce">
          {notification}
        </div>
      )}

      <header className="h-14 flex items-center justify-between px-5 border-b border-[#1e293b] bg-[#0f172a]/90 backdrop-blur-sm flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
            🦌 DeerFlow-X
          </div>
          <span className="text-xs text-[#64748b] bg-[#1e293b] px-2 py-0.5 rounded-full">SoloPreneurs OS</span>
        </div>

        <nav className="flex items-center gap-1">
          {navItems.map(item => (
            <button
              key={item.key}
              onClick={() => setView(item.key)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                view === item.key
                  ? 'bg-indigo-600 text-white'
                  : 'text-[#94a3b8] hover:text-white hover:bg-[#1e293b]'
              }`}
            >
              <item.icon className="w-3.5 h-3.5" />
              {item.label}
            </button>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          <a href="https://github.com" target="_blank" rel="noopener" className="text-[#94a3b8] hover:text-white transition-colors">
            <GitBranch className="w-4 h-4" />
          </a>
          <button className="flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium px-3 py-1.5 rounded-lg transition-colors">
            <Plus className="w-3.5 h-3.5" />
            新建项目
          </button>
          <div className="flex items-center gap-1.5 bg-[#1e293b] rounded-full pl-3 pr-1 py-1">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
            <span className="text-xs text-[#94a3b8]">v0.1.0</span>
            <ChevronDown className="w-3 h-3 text-[#64748b]" />
          </div>
        </div>
      </header>

      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="px-5 py-4 border-b border-[#1e293b] flex-shrink-0">
          <StatsPanel stats={stats} />
        </div>

        <div className="flex-1 overflow-hidden">
          {view === 'projects' && (
            <div className="flex gap-4 p-5 h-full">
              <ProjectSidebar
                projects={projects}
                selectedId={selectedProjectId}
                onSelect={id => { setSelectedProjectId(id); setSelectedTask(null); }}
              />
              <div className="flex-1 overflow-hidden">
                <div className="flex items-center justify-between mb-3">
                  <div>
                    <h2 className="text-base font-semibold" style={{ color: selectedProject.color }}>
                      {selectedProject.name}
                    </h2>
                    <p className="text-xs text-[#94a3b8] mt-0.5">{selectedProject.description}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="flex -space-x-2">
                      {selectedProject.agents.slice(0, 5).map(a => (
                        <div key={a.id} className="w-7 h-7 rounded-full bg-[#1e293b] border-2 border-[#0f172a] flex items-center justify-center text-sm"
                          title={`${a.name} (${a.role})`}>{a.avatar}</div>
                      ))}
                      {selectedProject.agents.length > 5 && (
                        <div className="w-7 h-7 rounded-full bg-[#334155] border-2 border-[#0f172a] flex items-center justify-center text-xs text-[#94a3b8]">
                          +{selectedProject.agents.length - 5}
                        </div>
                      )}
                    </div>
                    <span className="text-xs text-[#94a3b8]">
                      {selectedProject.completedTasks}/{selectedProject.taskCount} 任务完成
                    </span>
                  </div>
                </div>
                <div className="h-[calc(100%-3rem)]">
                  <TaskBoard
                    tasks={selectedProject.tasks}
                    selectedId={selectedTask?.id}
                    onSelect={setSelectedTask}
                  />
                </div>
              </div>
              <TaskDetailPanel task={selectedTask} onClose={() => setSelectedTask(null)} />
            </div>
          )}

          {view === 'team' && (
            <div className="p-5 h-full overflow-hidden">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-base font-semibold">🤖 AI 团队</h2>
                  <p className="text-xs text-[#94a3b8] mt-0.5">
                    共 {stats.totalAgents} 个 Agent，{stats.runningAgents} 个在线
                  </p>
                </div>
                <div className="flex items-center gap-4 text-xs">
                  <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-green-500" /> 在线</span>
                  <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-amber-500" /> 忙碌</span>
                  <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-gray-500" /> 离线</span>
                </div>
              </div>
              <TeamView agents={projects.flatMap(p => p.agents).filter((a, i, arr) => arr.findIndex(x => x.id === a.id) === i)} />
            </div>
          )}

          {view === 'analytics' && <AnalyticsView projects={projects} />}

          {view === 'deploy' && (
            <div className="p-5 max-w-2xl">
              <DeployPanel deployments={deployments} onDeploy={async (name) => {
                await triggerDeploy(name);
                notify(`${name} 部署成功！`);
              }} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function AnalyticsView({ projects }: { projects: ReturnType<typeof getProjects> }) {
  return (
    <div className="p-5 overflow-y-auto h-full">
      <h2 className="text-base font-semibold mb-4">📊 项目统计</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {projects.map(p => (
          <div key={p.id} className="bg-[#1e293b] rounded-xl border border-[#334155] p-4">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: p.color }} />
              <span className="font-medium text-sm">{p.name}</span>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-xs text-[#94a3b8]">
                <span>整体进度</span><span className="font-medium text-white">{p.progress}%</span>
              </div>
              <div className="h-2 bg-[#0f172a] rounded-full overflow-hidden">
                <div className="h-full rounded-full transition-all" style={{ width: `${p.progress}%`, backgroundColor: p.color }} />
              </div>
              <div className="flex justify-between text-xs text-[#94a3b8]">
                <span>任务完成</span><span className="font-medium text-white">{p.completedTasks}/{p.taskCount}</span>
              </div>
              <div className="flex justify-between text-xs text-[#94a3b8]">
                <span>参与成员</span><span className="font-medium text-white">{p.agents.length}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
