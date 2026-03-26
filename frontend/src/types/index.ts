// DeerFlow-X Type Definitions

export type AgentRole = 
  | 'CEO'
  | 'Architect'
  | 'Frontend Dev'
  | 'Backend Dev'
  | 'QA Engineer'
  | 'DevOps'
  | 'Product Manager'
  | 'Designer'
  | 'Data Analyst'
  | 'Security Engineer';

export type AgentStatus = 'online' | 'offline' | 'busy';

export interface Agent {
  id: string;
  name: string;
  role: AgentRole;
  avatar: string;
  status: AgentStatus;
  currentTask?: string;
  lastActive: string;
}

export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed' | 'queued';

export interface Task {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  assignee?: Agent;
  progress: number; // 0-100
  createdAt: string;
  updatedAt: string;
  output?: string;
  logs?: string[];
  tags?: string[];
}

export interface Project {
  id: string;
  name: string;
  description: string;
  color: string;
  status: 'active' | 'paused' | 'completed';
  taskCount: number;
  completedTasks: number;
  createdAt: string;
  agents: Agent[];
  tasks: Task[];
  progress: number;
}

export interface DashboardStats {
  totalProjects: number;
  activeProjects: number;
  totalTasks: number;
  completedTasks: number;
  runningAgents: number;
  totalAgents: number;
}

export interface DeploymentTarget {
  name: string;
  status: 'idle' | 'deploying' | 'success' | 'failed';
  url?: string;
  lastDeployed?: string;
}
