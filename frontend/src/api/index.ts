import type { DashboardStats, DeploymentTarget } from '../types';
import { mockStats, mockDeployments, mockProjects } from './mockData';

const API_BASE = 'http://localhost:8000';

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) throw new Error(`API ${path} failed: ${res.status}`);
  return res.json();
}

export async function fetchHealth() {
  return apiFetch<{ status: string; service: string; version: string }>('/health');
}

export async function createTask(task: { task: string; context?: Record<string, unknown> }) {
  return apiFetch<{ task_id: string; status: string; result: unknown }>('/tasks', {
    method: 'POST',
    body: JSON.stringify(task),
  });
}

export function getStats(): DashboardStats {
  return mockStats;
}

export function getDeployments(): DeploymentTarget[] {
  return mockDeployments;
}

export function getProjects() {
  return mockProjects;
}

export async function triggerDeploy(target: string): Promise<{ success: boolean; message: string }> {
  await new Promise(r => setTimeout(r, 2000));
  return { success: true, message: `${target} 部署已触发` };
}
