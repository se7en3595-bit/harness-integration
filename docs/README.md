# AI Agent Harness 生态系统

一个融合了Gyro四层工程约束和Gar Tan三层复利架构的完整AI代理测试与优化平台。

## 🎯 设计理念

### 来自Gyro的四层工程约束
1. **Super Powers** (纪律层) - 7阶段强制工作流
2. **GSD** (上下文层) - 200k token上下文隔离
3. **G-Stack** (角色层) - 23个专家角色审查
4. **Archon** (编排层) - YAML DAG工作流编排

### 来自Gar Tan的三层复利架构
1. **薄壳层** (调度器) - 只做路由的轻量调度
2. **厚技能层** (Skillify机制) - 自动生成优化的技能库
3. **厚数据层** (Brain Page) - 结构化知识图谱积累

## 🏗️ 融合架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Super Powers (纪律层)                     │
│  7个强制阶段：脑暴→Git隔离→方案→执行→TDD→审查→完成          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        GSD (上下文层)                       │
│  200k token上下文隔离 + 持久化artifacts + 原子任务循环      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      G-Stack (角色层)                       │
│  23个专家角色 + 多视角审查 + 决策质量保障                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Archon (编排层)                        │
│  YAML DAG工作流 + 并行执行 + 可观测性仪表板                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Gar Tan 三层复利系统                     │
│  薄壳调度 + Skillify生成 + Brain Page数据复利               │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 核心模块

### 1. Super Powers引擎 (`super_powers.py`)
**Gyro的第一层：纪律约束**
- 7个强制阶段的工作流控制
- Git worktree隔离实验环境
- TDD强制测试驱动开发
- 代码审查双重验证

**关键特性**：
```python
# 创建会话（强制7阶段）
session_id = engine.create_session("AI Enhancement", "requirements")

# 推进到执行阶段
engine.advance_to_stage(session_id, "execution")

# 强制TDD验证
engine.force_stage_validation(session_id, "tdd")
```

### 2. GSD上下文管理器 (`gsd_engine.py`) 
**Gyro的第二层：上下文隔离**
- 每个原子任务200k token新鲜上下文
- 持久化artifacts存储
- 6阶段命令循环：new-project→discuss→plan→execute→verify→ship

**关键特性**：
```python
# 启动新项目
result = gsd.run_command("/gsd-new-project", {"name": "my_project"})

# 执行原子任务（全新上下文）
result = gsd.run_command("/gsd-execute-phase", {"task": "implement_feature"})
```

### 3. G-Stack角色系统 (`gstack_roles.py`)
**Gyro的第三层：多角色审查**
- 23个专家角色：CEO、PM、工程师、QA、安全官等
- 多视角决策支持
- 阶段化角色调用

**关键特性**：
```python
# 召集产品讨论
ceo_review = gstack.call_role("/office-hours", ["ceo", "pm", "engineer"])

# CEO审查方案
ceo_feedback = gstack.call_role("/plan-ceo-review", {"plan": my_plan})
```

### 4. Gar Tan三层复利系统 (`gary_tan_system.py`)
**个人知识复利架构**

#### 薄壳调度层
- **核心原则**：只做路由，不塞业务逻辑
- **实现**：轻量调度器 + 技能注册表
- **优势**：系统脆弱性最小化

#### 厚技能层 (Skillify)
- **Skillify机制**：手工操作→生成技能→自动优化
- **质量迭代**：发现问题→skillify修复→永久受益
- **技能网络**：底层技能改进提升所有上层工作流

#### 厚数据层 (Brain Page)
- **结构化知识图谱**：每个人/公司/概念都有独立页面
- **持续积累**：会议笔记、书籍镜像、文章标签
- **复利效应**：数据越厚，理解越深，输出越准

**关键公式**：
```
竞争优势 = 模型(引擎) + 技能文件 + 数据积累 + 关系网络
```

## 🚀 使用方式

### 快速开始：选择你的层次

```bash
# 第一层：个人日常开发 - Super Powers
python super_powers.py --create-session "MyProject"

# 第二层：长任务管理 - GSD
python gsd_engine.py --new-project "ComplexTask"

# 第三层：多视角决策 - G-Stack
python gstack_roles.py --call-role ceo --plan "NewFeature"

# 复利系统：个人知识管理
python gary_tan_system.py --mirror-book "WhenThingsFallApart"
```

### 分层演进路径

1. **新手阶段**：Super Powers → 建立编程纪律
2. **进阶阶段**：+ GSD → 处理复杂长任务
3. **专家阶段**：+ G-Stack → 多视角决策支持
4. **团队阶段**：+ Archon → 规模化流程管理
5. **个人复利**：+ Gar Tan三层系统 → 构建专属知识资产

## 📊 性能对比

| 维度 | Super Powers | GSD | G-Stack | Archon | Gar Tan系统 |
|------|-------------|-----|---------|--------|-------------|
| 适用场景 | 个人日常 | 长任务 | 决策支持 | 团队协作 | 个人复利 |
| 学习曲线 | ⭐☆☆☆☆ | ⭐⭐☆☆☆ | ⭐⭐⭐☆☆ | ⭐⭐⭐⭐☆ | ⭐⭐☆☆☆ |
| 维护成本 | 低 | 中 | 中高 | 高 | 中 |
| 复利效应 | 无 | 有限 | 有限 | 有限 | 指数级 |

## 🛠️ 技术架构

### 统一接口设计
```python
class HarnessInterface:
    """所有harness的统一接口"""
    
    async def validate_stage(self, stage_config: Dict) -> ValidationResult:
        pass
    
    async def execute_task(self, task_spec: TaskSpec) -> ExecutionResult:
        pass
    
    async def collect_metrics(self) -> MetricsData:
        pass
```

### 模型调度策略 (Gar Tan理念)
- **Opus 4.7**: 高精度处理
- **GPT-5.5**: 召回和穷举提取
- **DeepSeek V4-Pro**: 创意视角
- **Groq + Llama**: 速度场景
- **动态切换**: 技能文件中配置模型调用

## 📈 成功案例

### Super Powers实战
> "我用它写一个数据导出功能，Agent在Execution阶段写完代码后，自动进入TDD阶段，发现我没给测试数据，直接停下来问我要mock data。这在裸跑Claude Code里是不可能的。"

### GSD实战  
> "重构一个15个文件的模块，拆成8个phase。每个phase都是新鲜上下文，Agent不会被前面的调试记录干扰。最后8个phase全部通过测试，git diff干净得像手写的。"

### Gar Tan复利系统
> "Book Mirror读了20本书，从第一本到第20本，每一本书的映射越来越精准，因为Brain Data越来越厚。这是真正的个人护城河。"

## 🔮 未来展望

### 智能层级叠加
不是四派互斥，而是四层叠加：
- **底层**：Super Powers纪律 → 让Agent不乱来
- **第二层**：GSD上下文 → 让长任务不腐烂  
- **第三层**：G-Stack角色 → 让视角不单一
- **最上层**：Archon编排 → 让团队流程标准化
- **个人层面**：Gar Tan复利 → 构建专属知识资产

---

*本harness系统深度整合了Gyro的四层工程约束思想和Gar Tan的三层复利架构理念，为AI代理的测试、评估、优化和个人知识管理提供了完整的解决方案谱系。*

**选择你的层次，构建你的AI工作体系！**