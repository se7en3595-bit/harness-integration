---
name: harness-integration
description: AI Agent Harness - 四层工程约束 + 三层复利系统 + Token优化，直接在牛马AI中调用
author: SE7EN
version: 0.8.0
tags: [harness, super-powers, gsd, g-stack, gar-tan, token-optimization, ai-engineering]
---

# AI Agent Harness Integration Skill

直接在牛马AI中调用完整的AI代理工程化框架，无需切换窗口。

## 🏗️ 架构概览

```
┌─────────────────────────────────────────────────┐
│              Token优化层                          │
│  智能缓存 | 上下文压缩 | 知识复用 | Prompt优化 | 监控 │
├─────────────────────────────────────────────────┤
│  第一层: Super Powers  → 7阶段状态机，硬门禁执行   │
│  第二层: GSD           → 6阶段项目管理，上下文隔离  │
│  第三层: G-Stack       → 关键词匹配评分，多角色审查 │
│  第四层: Archon        → DAG工作流编排（计划中）    │
├─────────────────────────────────────────────────┤
│  薄壳调度  →  Skillify自动生成  →  Brain Page积累  │
└─────────────────────────────────────────────────┘
```

## 🚀 快速命令

### 系统状态
```
/harness status
```

### Super Powers（第一层：编程纪律）
```
/harness super-powers create-session '{"project": "任务名称"}'
/harness super-powers advance '{"session_id": "xxx", "checklist_completed": ["需求确认"]}'
/harness super-powers status '{"session_id": "xxx"}'
/harness super-powers list-stages
/harness super-powers list-sessions
```

### GSD（第二层：上下文隔离）
```
/harness gsd new-project '{"name": "项目名称", "description": "描述"}'
/harness gsd execute-phase '{"project_id": "xxx", "task": "原子任务", "command": "/gsd-execute-phase"}'
/harness gsd run-command '{"project_id": "xxx", "command": "/gsd-plan-phase", "plan_items": ["步骤1"]}'
/harness gsd status '{"project_id": "xxx"}'
/harness gsd list-projects
```

### G-Stack（第三层：多角色决策）
```
/harness g-stack office-hours '{"topic": "讨论主题", "content": "方案内容"}'
/harness g-stack recommend-roles '{"topic": "主题"}'
/harness g-stack list-roles
/harness g-stack history
```

### Gar Tan（三层复利系统）
```
/harness gar-tan mirror-book '{"title": "书名", "content": "书的内容"}'
/harness gar-tan analyze-meeting '{"transcript": "会议记录", "participants": "张三,李四"}'
/harness gar-tan query '{"query": "搜索关键词"}'
/harness gar-tan dashboard
```

### Token优化
```
/harness token status
/harness token optimize-prompt '{"prompt": "长prompt", "budget": 5000}'
/harness token compress-context '{"context": [...]}'
/harness token cache-stats
```

### Token监控
```
/harness monitor stats
/harness monitor suggestions
/harness monitor report
/harness monitor record '{"module": "gsd", "action": "execute", "tokens_in": 500, "tokens_out": 200}'
```

## 💡 使用案例

### 案例1：开始新功能开发
```
/harness super-powers create-session '{"project": "实现用户权限管理系统"}'
```
→ 创建7阶段会话，强制从需求脑暴开始，不允许跳过

### 案例2：处理复杂重构
```
/harness gsd new-project '{"name": "API权限模块重构"}'
/harness gsd run-command '{"project_id": "xxx", "command": "/gsd-execute-phase", "task": "设计新权限架构"}'
```
→ 每个 execute phase 记录上下文隔离快照，artifacts 跨阶段持久化

### 案例3：产品决策
```
/harness g-stack office-hours '{"topic": "数据导出功能设计", "content": "方案描述..."}'
```
→ 基于内容关键词与角色职责匹配评分，自动推荐相关角色

### 案例4：学习积累
```
/harness gar-tan mirror-book '{"title": "书名", "content": "章节内容..."}'
```
→ 提取概念写入内存知识图谱，支持后续 query 检索

## 🔍 各模块实现状态

| 模块 | 状态 | 实现说明 |
|------|------|---------|
| Super Powers | ✅ 已实现 | 真实7阶段状态机，硬门禁强制执行 |
| GSD | ✅ 已实现 | 真实6阶段项目管理，上下文隔离记录 |
| G-Stack | ✅ 已实现 | 基于关键词匹配的角色评分（非AI调用） |
| Gar Tan | ✅ 已实现 | 内存知识图谱，Jaccard相似度搜索 |
| Token缓存 | ✅ 已实现 | LRU + 模式匹配 + 上下文复用三级缓存 |
| Token压缩 | ✅ 已实现 | 去噪 + 关键状态提取 |
| Token监控 | ✅ 已实现 | 实时统计 + 告警 + 报告 |
| Archon | 🔲 计划中 | YAML DAG工作流编排 |
| 知识图谱持久化 | 🔲 计划中 | 当前为内存存储，重启后清空 |

## 🎯 演进路径

```
Day 1:   Super Powers → 建立编程纪律
Week 1:  + GSD        → 管理长任务上下文
Month 1: + G-Stack    → 多视角决策质量
Long:    + Gar Tan    → 个人知识积累
```

## 💎 核心理念

**Gyro**: "这不是模型问题，是工程约束问题。这就是Harness要解决的事。"

**Gar Tan**: "竞争优势 = 模型引擎 + 技能文件 + 数据积累 + 关系网络"

## ⚠️ 注意事项

- 核心功能仅需 Python 3.8+ 标准库，无需安装第三方包
- `rich`、`matplotlib` 为可选依赖，缺少时自动降级为标准输出
- Gar Tan 知识图谱当前为内存存储，进程重启后数据清空
- G-Stack 评分基于关键词匹配，不调用 AI 模型
