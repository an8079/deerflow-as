import type { Agent, Project, Task, DashboardStats, DeploymentTarget } from '../types';

export const mockAgents: Agent[] = [
  { id: '1', name: 'Chief AI Officer', role: 'CEO', avatar: '👔', status: 'online', currentTask: '规划 Q2 路线图', lastActive: new Date().toISOString() },
  { id: '2', name: 'System Architect', role: 'Architect', avatar: '🏗️', status: 'online', currentTask: '设计微服务架构', lastActive: new Date(Date.now() - 300000).toISOString() },
  { id: '3', name: 'Frontend Engineer', role: 'Frontend Dev', avatar: '⚛️', status: 'busy', currentTask: '实现仪表盘 UI', lastActive: new Date(Date.now() - 60000).toISOString() },
  { id: '4', name: 'Backend Engineer', role: 'Backend Dev', avatar: '⚡', status: 'online', currentTask: 'API 路由开发', lastActive: new Date(Date.now() - 120000).toISOString() },
  { id: '5', name: 'QA Engineer', role: 'QA Engineer', avatar: '🔍', status: 'offline', currentTask: '待命', lastActive: new Date(Date.now() - 7200000).toISOString() },
  { id: '6', name: 'DevOps Engineer', role: 'DevOps', avatar: '🚀', status: 'busy', currentTask: 'CI/CD 配置', lastActive: new Date(Date.now() - 300000).toISOString() },
  { id: '7', name: 'Product Manager', role: 'Product Manager', avatar: '📋', status: 'online', currentTask: '用户调研分析', lastActive: new Date(Date.now() - 900000).toISOString() },
  { id: '8', name: 'UI/UX Designer', role: 'Designer', avatar: '🎨', status: 'online', currentTask: '设计系统搭建', lastActive: new Date(Date.now() - 600000).toISOString() },
  { id: '9', name: 'Data Analyst', role: 'Data Analyst', avatar: '📊', status: 'offline', currentTask: '待命', lastActive: new Date(Date.now() - 14400000).toISOString() },
  { id: '10', name: 'Security Engineer', role: 'Security Engineer', avatar: '🔒', status: 'online', currentTask: '渗透测试报告', lastActive: new Date(Date.now() - 450000).toISOString() },
];

const tasks1: Task[] = [
  { id: 't1', title: '实现项目仪表盘', description: '左侧项目列表 + 右侧任务看板', status: 'running', assignee: mockAgents[2], progress: 75, createdAt: new Date(Date.now() - 3600000).toISOString(), updatedAt: new Date().toISOString(), output: '完成 5 个组件，预计今天完成', tags: ['frontend', 'ui'] },
  { id: 't2', title: '设计 RESTful API', description: '用户、项目、任务相关接口', status: 'completed', assignee: mockAgents[3], progress: 100, createdAt: new Date(Date.now() - 86400000).toISOString(), updatedAt: new Date(Date.now() - 43200000).toISOString(), output: '完成 12 个 API 端点', tags: ['backend', 'api'] },
  { id: 't3', title: '配置 Docker 环境', description: '多服务容器编排', status: 'running', assignee: mockAgents[5], progress: 40, createdAt: new Date(Date.now() - 7200000).toISOString(), updatedAt: new Date().toISOString(), tags: ['devops'] },
  { id: 't4', title: '安全漏洞扫描', description: 'OWASP Top 10 扫描', status: 'queued', assignee: mockAgents[9], progress: 0, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(), tags: ['security'] },
];

const tasks2: Task[] = [
  { id: 't5', title: '用户调研报告', description: '目标用户访谈与需求收集', status: 'completed', assignee: mockAgents[6], progress: 100, createdAt: new Date(Date.now() - 172800000).toISOString(), updatedAt: new Date(Date.now() - 86400000).toISOString(), output: '访谈 10 位用户，输出 3 个 persona', tags: ['product'] },
  { id: 't6', title: '设计系统文档', description: '颜色、字体、组件规范', status: 'running', assignee: mockAgents[7], progress: 60, createdAt: new Date(Date.now() - 259200000).toISOString(), updatedAt: new Date().toISOString(), tags: ['design'] },
  { id: 't7', title: '数据埋点方案', description: '埋点事件设计与采集', status: 'pending', assignee: mockAgents[8], progress: 0, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(), tags: ['data'] },
];

const tasks3: Task[] = [
  { id: 't8', title: 'LangGraph 工作流', description: '多 Agent 调度引擎', status: 'running', assignee: mockAgents[1], progress: 30, createdAt: new Date(Date.now() - 43200000).toISOString(), updatedAt: new Date().toISOString(), output: '设计图完成，编码中...', tags: ['architecture'] },
  { id: 't9', title: '数据库 Schema', description: 'Postgres 数据模型设计', status: 'completed', assignee: mockAgents[3], progress: 100, createdAt: new Date(Date.now() - 259200000).toISOString(), updatedAt: new Date(Date.now() - 172800000).toISOString(), output: '8 张表，含索引和约束', tags: ['backend', 'database'] },
];

export const mockProjects: Project[] = [
  { id: 'p1', name: 'DeerFlow-X 主系统', description: 'AI 团队协作操作系统核心开发', color: '#6366f1', status: 'active', taskCount: 4, completedTasks: 1, createdAt: new Date(Date.now() - 604800000).toISOString(), agents: mockAgents.slice(0, 6), tasks: tasks1, progress: 52 },
  { id: 'p2', name: 'SoloPreneurs Pro', description: '商业化变现功能模块', color: '#f59e0b', status: 'active', taskCount: 3, completedTasks: 1, createdAt: new Date(Date.now() - 259200000).toISOString(), agents: mockAgents.slice(5, 9), tasks: tasks2, progress: 53 },
  { id: 'p3', name: '智能调度引擎', description: '基于 LangGraph 的多 Agent 工作流', color: '#22c55e', status: 'active', taskCount: 2, completedTasks: 1, createdAt: new Date(Date.now() - 172800000).toISOString(), agents: [mockAgents[0], mockAgents[1], mockAgents[3]], tasks: tasks3, progress: 65 },
  { id: 'p4', name: '移动端适配', description: '响应式设计 + PWA 支持', color: '#ec4899', status: 'paused', taskCount: 5, completedTasks: 0, createdAt: new Date(Date.now() - 1209600000).toISOString(), agents: [mockAgents[2], mockAgents[7]], tasks: [], progress: 0 },
];

export const mockStats: DashboardStats = {
  totalProjects: 4,
  activeProjects: 3,
  totalTasks: 14,
  completedTasks: 3,
  runningAgents: 5,
  totalAgents: 10,
};

export const mockDeployments: DeploymentTarget[] = [
  { name: 'Vercel (Frontend)', status: 'success', url: 'https://deer-flow-x.vercel.app', lastDeployed: new Date(Date.now() - 3600000).toISOString() },
  { name: 'Railway (Backend)', status: 'deploying', lastDeployed: new Date().toISOString() },
  { name: 'Supabase (Database)', status: 'success', url: 'https://supabase.com/dashboard', lastDeployed: new Date(Date.now() - 86400000).toISOString() },
];
