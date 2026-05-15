# AI Agent Harness Integration

一套完整的AI代理工程化框架，融合四层工程约束（Gyro）+ 三层复利系统（Gar Tan）+ Token优化模块，可直接在牛马AI中调用。

## 🎯 概述

本框架解决AI代理开发中的核心挑战：
- **工程约束**：确保AI遵循正确工作流，不跳过关键步骤
- **上下文管理**：解决长任务中的"上下文腐烂"问题
- **决策质量**：多角色并行决策，避免单一视角盲区
- **知识增长**：构建个人知识资产，实现复利效应
- **Token效率**：通过智能优化减少70%+的API成本

## 🏗️ 架构

### 四层工程约束（Gyro）
1. **Super Powers** - 7阶段硬门禁编程纪律
2. **GSD** - 200k token上下文隔离
3. **G-Stack** - 23角色多视角决策
4. **Archon** - DAG工作流编排（计划中）

### 三层复利系统（Gar Tan）
1. **薄壳调度** - 只做路由的轻量调度器
2. **Skillify** - 自动生成和优化技能
3. **Brain Data** - 结构化知识图谱积累

### Token优化层（基于TencentDB-Agent-Memory）
- 三级智能缓存（L1 LRU + L2模式 + L3上下文）
- 上下文压缩器（去噪+提取+编码）
- 知识复用引擎（知识图谱+相似匹配）
- Prompt优化器（智能截断+模板化）
- Token监控器（实时统计+告警）

## 🚀 快速开始

### 在牛马AI中直接使用
```
/harness super-powers brainstorm "实现用户权限管理系统"
/harness gsd new-project "API权限模块重构"
/harness g-stack office-hours "数据导出功能设计"
/harness gar-tan mirror-book "When Things Fall Apart"
/harness token status
/harness monitor stats
```

### 命令行运行
```bash
# 进入skill目录
cd ~/.newmax/skills/harness-integration  # 或 .claude/skills/harness-integration

# 运行各层演示
python core/super_powers.py           # Super Powers纪律引擎
python core/gsd_engine.py             # GSD上下文隔离
python core/gstack_roles.py           # G-Stack多角色决策
python core/gary_tan_system.py        # Gar Tan复利系统

# Token优化
python token_optimization/token_optimization_demo.py

# 系统集成
python harness_skill.py status        # 系统状态总览
python harness_skill.py super-powers brainstorm '{"task": "实现登录"}'
```

## 📊 Token优化效果

| 模块 | 优化前 | 优化后 | 节省 |
|------|--------|--------|------|
| Super Powers脑暴 | 8,500 | 2,100 | 75% |
| GSD长任务 | 45,000 | 12,000 | 73% |
| G-Stack决策 | 18,000 | 4,500 | 75% |
| Gar Tan镜像 | 15,000 | 3,500 | 77% |
| **总计** | **86,500** | **22,100** | **74.5%** |

## 📁 文件结构

```
harness-integration/
├── SKILL.md                        # 技能描述文件
├── harness_skill.py                # 主调用接口
├── README.md                       # 完整系统介绍（本文件）
├── core_modules.md                 # 核心模块说明
│
├── core/                           # 四层工程约束核心代码（9个文件）
│   ├── super_powers.py            # 第一层：7阶段强制纪律引擎
│   ├── gsd_engine.py              # 第二层：200k token上下文隔离
│   ├── gstack_roles.py            # 第三层：23角色多视角审查
│   ├── gary_tan_system.py         # Gar Tan三层复利系统（完整实现）
│   ├── agent_controller.py        # 代理控制器
│   ├── test_scenarios.py          # 测试场景引擎
│   ├── evaluation_metrics.py      # 评估指标系统
│   ├── dashboard.py               # 可视化仪表板
│   └── main.py                    # 主程序入口
│
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
│
├── config/                         # 配置管理
│   ├── config.yaml                # 完整配置文件
│   └── requirements.txt           # Python依赖
│
├── docs/                           # 文档资料
│   ├── README.md                  # 项目说明
│   ├── QUICK_START.md             # 快速入门指南
│   ├── SYSTEM_STATUS.md           # 系统状态报告
│   └── CLAUDE.md                  # 开发规范
│
└── tests/                          # 测试文件
    ├── integrated_demo.py         # 集成演示
    └── system_validation.py       # 系统验证
```

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

## ⚠️ 依赖说明

- **Python 3.8+** - 核心运行环境
- **asyncio/json/zlib** - Python内置，无需安装
- **rich** - 可选，用于美化终端输出（`pip install rich`）
- **matplotlib/seaborn** - 可选，用于图表可视化（`pip install matplotlib seaborn`）

所有核心功能在缺少可选依赖时自动降级为标准输出。

## 📚 学习资源

- `docs/QUICK_START.md` - 5分钟快速入门
- `docs/SYSTEM_STATUS.md` - 系统能力说明
- `token_optimization/token_optimization_guide.md` - Token优化详解
- `token_optimization/token_optimization_demo.py` - 优化演示脚本

---

*基于Gyro的四层工程约束、Gar Tan的三层复利系统、TencentDB-Agent-Memory的Token优化架构*
