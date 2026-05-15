---
name: harness-integration
description: AI Agent Harness 集成工具 - 四层工程约束 + 三层复利系统 + Token优化（节省74.5%）
author: SE7EN
version: 2.1.0
tags: [harness, super-powers, gsd, g-stack, gar-tan, token-optimization, ai-engineering]
---

# AI Agent Harness Integration Skill

直接在牛马AI中调用完整的AI代理工程化框架，无需切换窗口。

## 🏗️ 架构概览

**四层工程约束（Gyro）+ 三层复利系统（Gar Tan）+ Token优化模块**

```
┌─────────────────────────────────────────────────┐
│              Token优化层 (节省74.5%)              │
│  智能缓存 | 上下文压缩 | 知识复用 | Prompt优化 | 监控 │
├─────────────────────────────────────────────────┤
│  第一层: Super Powers     → 编程纪律（7阶段硬门禁） │
│  第二层: GSD              → 上下文隔离（200k fresh）│
│  第三层: G-Stack          → 多角色决策（23角色）   │
│  第四层: Archon (计划中)   → DAG工作流编排         │
├─────────────────────────────────────────────────┤
│  薄壳调度  →  Skillify自动生成  →  Brain Page积累  │
└─────────────────────────────────────────────────┘
```

## 🚀 快速命令

### 系统状态
```
/harness status
```

### Super Powers (第一层: 纪律)
```
/harness super-powers brainstorm "任务描述"
/harness super-powers tdd-check "代码片段"
/harness super-powers git-isolate "项目名称"
/harness super-powers status
```

### GSD (第二层: 上下文隔离)
```
/harness gsd new-project "项目名称"
/harness gsd execute-phase "原子任务"
/harness gsd verify-work "检查结果"
/harness gsd status
```

### G-Stack (第三层: 多角色决策)
```
/harness g-stack office-hours "讨论主题"
/harness g-stack role-review "ceo"
/harness g-stack list-roles
```

### Gar Tan (复利系统)
```
/harness gar-tan mirror-book "书名"
/harness gar-tan analyze-meeting "会议记录"
/harness gar-tan knowledge-graph
/harness gar-tan brain-page "page_id"
```

### Token优化
```
/harness token status
/harness token optimize-prompt "长prompt"
/harness token compress-context
/harness token cache-stats
```

### Token监控
```
/harness monitor stats
/harness monitor suggestions
/harness monitor report
```

## 💡 使用案例

### 案例1：开始新功能开发
```
/harness super-powers brainstorm "实现用户权限管理系统"
```
→ 强制需求脑暴，防止模糊需求直接进入开发

### 案例2：处理复杂重构
```
/harness gsd new-project "API权限模块重构"
/harness gsd execute-phase "设计新的权限架构"
```
→ 每个phase都是200k fresh context，无历史噪音

### 案例3：产品决策
```
/harness g-stack office-hours "数据导出功能设计"
```
→ 多角色并行讨论，避免单一视角盲区

### 案例4：学习积累
```
/harness gar-tan mirror-book "When Things Fall Apart"
```
→ 书籍镜像到知识图谱，积累个人知识护城河

### 案例5：Token优化
```
/harness token status
```
→ 查看各模块token节省效果

## 📊 Token优化效果

| 模块 | 优化前 | 优化后 | 节省 |
|------|--------|--------|------|
| Super Powers脑暴 | 8,500 | 2,100 | 75% |
| GSD长任务 | 45,000 | 12,000 | 73% |
| G-Stack决策 | 18,000 | 4,500 | 75% |
| Gar Tan镜像 | 15,000 | 3,500 | 77% |
| **总计** | **86,500** | **22,100** | **74.5%** |

## 🎯 演进路径

```
Day 1:   Super Powers → 建立编程纪律
Week 1:  + GSD        → 管理长任务上下文
Month 1: + G-Stack    → 多视角决策质量
Long:    + Gar Tan    → 个人知识护城河
Always:  + Token优化  → 持续节省token消耗
```

## 💎 核心理念

**Gyro**: "这不是模型问题，是工程约束问题。这就是Harness要解决的事。"

**Gar Tan**: "竞争优势 = 模型引擎 + 技能文件 + 数据积累 + 关系网络"

## 📁 文件结构

```
harness-integration/
├── SKILL.md                        # 技能描述（本文件）
├── harness_skill.py                # 主调用接口
├── README.md                       # 完整系统介绍
├── core_modules.md                 # 核心模块说明
├── core/                           # 四层工程约束核心代码（9个文件）
│   ├── super_powers.py            # 第一层：7阶段强制纪律
│   ├── gsd_engine.py              # 第二层：200k上下文隔离
│   ├── gstack_roles.py            # 第三层：23角色多视角审查
│   ├── gary_tan_system.py         # Gar Tan三层复利系统
│   ├── agent_controller.py        # 代理控制器
│   ├── test_scenarios.py          # 测试场景引擎
│   ├── evaluation_metrics.py      # 评估指标系统
│   ├── dashboard.py               # 可视化仪表板
│   └── main.py                    # 主程序入口
├── token_optimization/             # Token优化模块（9个文件）
│   ├── config.yaml                # 优化配置
│   ├── README.md                  # 优化模块文档
│   ├── token_optimizer.py         # 核心优化引擎
│   ├── cache_manager.py           # 三级智能缓存
│   ├── context_compressor.py      # 上下文压缩器
│   ├── knowledge_reuse.py         # 知识复用引擎
│   ├── prompt_optimizer.py        # Prompt优化器
│   ├── token_monitor.py           # Token监控器
│   ├── token_optimization_demo.py # 演示脚本
│   └── token_optimization_guide.md# 详细使用指南
├── config/                         # 配置管理
│   ├── config.yaml                # 完整配置文件
│   └── requirements.txt           # Python依赖
├── docs/                           # 文档资料
│   ├── README.md                  # 项目说明
│   ├── QUICK_START.md             # 快速入门
│   ├── SYSTEM_STATUS.md           # 系统状态
│   └── CLAUDE.md                  # 开发规范
└── tests/                          # 测试文件
    ├── integrated_demo.py         # 集成演示
    └── system_validation.py       # 系统验证
```

## ⚠️ 注意事项

- **依赖**：核心功能仅需Python 3.8+标准库。rich和matplotlib为可选依赖
- **建议**：从Super Powers开始，逐步叠加其他层次
- **Token优化**：默认启用，无需手动开启
- **知识图谱**：数据持久化存储，长期积累复利效应
