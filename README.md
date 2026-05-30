# AI Agent Harness v0.8

融合四层工程约束（Gyro）+ 三层复利系统（Gar Tan）+ Token优化模块的AI代理工程化框架，可直接在牛马AI中调用。

## 🎯 解决什么问题

- **工程约束**：AI 容易跳过 TDD、跳过需求确认直接写代码。Super Powers 用状态机强制执行7个阶段，每个阶段都是硬门禁
- **上下文腐烂**：长任务中调试记录、废弃方案会污染后续上下文。GSD 把大任务拆成原子阶段，每个 execute phase 记录隔离快照
- **单一视角**：一个 AI 自己审自己容易有盲区。G-Stack 让多个角色基于各自职责关键词独立评分
- **知识流失**：每次对话结束知识就消失。Gar Tan 把书籍、会议内容写入内存知识图谱，支持检索复用

## 🏗️ 架构

### 四层工程约束（Gyro）

**第一层 Super Powers** (`core/super_powers.py`)
- 真实7阶段状态机：脑暴 → Git隔离 → 规划 → 执行 → TDD → 审查 → 完成
- 每个阶段都是硬门禁，`advance()` 检查 checklist 完成情况才允许推进
- 不依赖外部 AI 调用，纯本地状态管理

**第二层 GSD** (`core/gsd_engine.py`)
- 真实6阶段项目管理：discuss → plan → execute → execute → verify → ship
- execute 阶段记录上下文隔离快照，保存已完成阶段列表和 artifacts 摘要
- artifacts（PLAN.md、DISCUSS.md、EXECUTE_N.md 等）跨阶段持久化

**第三层 G-Stack** (`core/gstack_roles.py`)
- 24个角色定义，每个角色有 focus 关注点和 scoring_criteria 评分标准
- `_review_as_role()` 检查内容中是否覆盖角色关注点，命中率映射到 [0.5, 1.0] 分数
- 不调用 AI 模型，基于关键词匹配评分
- `recommend_roles()` 根据 topic 关键词自动推荐 2-4 个相关角色

**第四层 Archon**（计划中）
- YAML DAG 工作流编排

### 三层复利系统（Gar Tan）

**薄壳调度** (`core/gary_tan_system.py` - `ThinShellScheduler`)
- 关键词评分路由，只做请求分发，不包含业务逻辑

**Skillify 引擎** (`core/gary_tan_system.py` - `SkillifyEngine`)
- 观察用户操作步骤，提取模式，生成可复用技能模板
- Jaccard 相似度匹配已有模板，相似时优化而非重复创建

**Brain Data** (`core/gary_tan_system.py` - `BrainDataManager`)
- 内存知识图谱，支持按标签和内容搜索
- 书籍镜像、会议分析结果写入对应 BrainPage
- 注意：当前为内存存储，进程重启后数据清空

### Token优化层

| 模块 | 文件 | 功能 |
|------|------|------|
| 缓存管理 | `token_optimization/cache_manager.py` | LRU + 模式匹配 + 上下文复用三级缓存 |
| 上下文压缩 | `token_optimization/context_compressor.py` | 去噪 + 关键状态提取 |
| 知识复用 | `token_optimization/knowledge_reuse.py` | Jaccard 相似度匹配已有知识 |
| Prompt优化 | `token_optimization/prompt_optimizer.py` | 智能截断 + 模板化 |
| Token监控 | `token_optimization/token_monitor.py` | 实时统计 + 告警 + 报告 |

## 🚀 快速开始

### 在牛马AI中使用

```bash
# 查看系统状态
/harness status

# Super Powers：创建开发会话
/harness super-powers create-session '{"project": "实现用户权限管理系统"}'

# GSD：创建长任务项目
/harness gsd new-project '{"name": "API权限模块重构"}'

# G-Stack：多角色讨论
/harness g-stack office-hours '{"topic": "数据导出功能设计", "content": "方案描述..."}'

# Gar Tan：书籍镜像
/harness gar-tan mirror-book '{"title": "书名", "content": "内容..."}'
```

### 命令行运行

```bash
cd E:/WorkSpace/Newmax/.claude/skills/harness-integration

# 各层演示
python core/super_powers.py
python core/gsd_engine.py
python core/gstack_roles.py
python core/gary_tan_system.py

# 主接口
python harness_skill.py status
python harness_skill.py super-powers create-session '{"project": "实现登录"}'
python harness_skill.py g-stack office-hours '{"topic": "API设计", "content": "RESTful接口方案"}'
```

## 🔍 实现状态

| 模块 | 状态 | 说明 |
|------|------|------|
| Super Powers | ✅ 已实现 | 真实状态机，硬门禁 |
| GSD | ✅ 已实现 | 真实项目管理，上下文隔离记录 |
| G-Stack | ✅ 已实现 | 关键词匹配评分，非AI调用 |
| Gar Tan | ✅ 已实现 | 内存知识图谱，Jaccard搜索 |
| Token缓存 | ✅ 已实现 | 三级缓存，LRU淘汰 |
| Token压缩 | ✅ 已实现 | 去噪+状态提取 |
| Token监控 | ✅ 已实现 | 实时统计+告警 |
| Archon | 🔲 计划中 | YAML DAG编排 |
| 知识图谱持久化 | 🔲 计划中 | 当前内存存储 |

## 📁 文件结构

```
harness-integration/
├── SKILL.md                        # 牛马AI技能描述
├── harness_skill.py                # 主调用接口（路由到各核心模块）
├── README.md                       # 本文件
├── core_modules.md                 # 核心模块说明
├── core/                           # 核心实现
│   ├── super_powers.py            # 第一层：7阶段状态机
│   ├── gsd_engine.py              # 第二层：6阶段项目管理
│   ├── gstack_roles.py            # 第三层：多角色评分
│   ├── gary_tan_system.py         # 三层复利系统
│   ├── agent_controller.py        # 代理控制器
│   ├── test_scenarios.py          # 测试场景
│   ├── evaluation_metrics.py      # 评估指标
│   ├── dashboard.py               # 可视化仪表板
│   └── main.py                    # 主程序入口
├── token_optimization/             # Token优化模块
│   ├── token_optimizer.py         # 优化引擎
│   ├── cache_manager.py           # 三级缓存
│   ├── context_compressor.py      # 上下文压缩
│   ├── knowledge_reuse.py         # 知识复用
│   ├── prompt_optimizer.py        # Prompt优化
│   ├── token_monitor.py           # 监控
│   ├── config.yaml                # 优化配置
│   └── token_optimization_guide.md
├── config/
│   ├── config.yaml
│   └── requirements.txt
├── docs/
│   ├── QUICK_START.md
│   ├── SYSTEM_STATUS.md
│   └── CLAUDE.md
└── tests/
    ├── integrated_demo.py
    └── system_validation.py
```

## ⚠️ 依赖说明

- **Python 3.8+**，核心功能仅用标准库，无需安装第三方包
- `rich` 可选，用于美化终端输出
- `matplotlib` 可选，用于图表可视化
- 缺少可选依赖时自动降级为标准输出

## 💎 核心理念

**Gyro**: "这不是模型问题，是工程约束问题。这就是Harness要解决的事。"

**Gar Tan**: "竞争优势 = 模型引擎 + 技能文件 + 数据积累 + 关系网络"

---

*基于 Gyro 的四层工程约束、Gar Tan 的三层复利系统、TencentDB-Agent-Memory 的 Token 优化架构*
