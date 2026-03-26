# 监控与告警
## 核心指标 (RED)
- Rate: QPS
- Errors: <0.1%
- Duration: P50/P95/P99
## 告警规则
| 错误率>1% | P2 Slack | >5% | P1 PagerDuty |
| P99>3s | P2 Slack | CPU>80% | 自动扩容 |
## 技术栈
日志: Loki/Promtail + Grafana
追踪: OpenTelemetry + Jaeger
指标: Prometheus + Grafana