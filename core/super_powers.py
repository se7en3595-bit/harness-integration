#!/usr/bin/env python3
"""
AI Agent Harness - Super Powers 纪律引擎（第一层）

基于Gyro的Super Powers理念：把"建议"变成"门禁"
7阶段强制工作流，防止AI跳过关键检查点

核心理念：
- 脑暴阶段：先想清楚要做什么，不急着动代码
- Git隔离：用worktree隔离实验，不污染主分支
- 规划阶段：写spec和PLAN，让人能审
- 执行阶段：开始写代码
- TDD阶段：先写测试，再让测试通过（RED-GREEN-REFACTOR）
- 审查阶段：自己审一遍，再让AI审一遍
- 完成阶段：确认测试通过，合并分支
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional


# ============================================================
# 7个强制阶段定义
# ============================================================

STAGES = [
    {
        "id": 1,
        "name": "brainstorming",
        "display_name": "需求脑暴",
        "description": "先想清楚要做什么，不急着动代码",
        "hard_gate": True,
        "checklist": [
            "明确功能需求和边界",
            "识别技术风险和依赖",
            "定义验收标准",
            "确认范围不蔓延"
        ]
    },
    {
        "id": 2,
        "name": "git_worktree",
        "display_name": "Git隔离",
        "description": "用worktree创建隔离实验环境",
        "hard_gate": True,
        "checklist": [
            "创建git worktree",
            "确认基础分支干净",
            "验证CI环境可用"
        ]
    },
    {
        "id": 3,
        "name": "planning",
        "display_name": "方案规划",
        "description": "写spec和PLAN文档",
        "hard_gate": True,
        "checklist": [
            "编写详细spec文档",
            "列出执行步骤PLAN",
            "预估时间和风险",
            "获得审核确认"
        ]
    },
    {
        "id": 4,
        "name": "execution",
        "display_name": "代码执行",
        "description": "按PLAN执行代码开发",
        "hard_gate": False,
        "checklist": [
            "按步骤执行PLAN",
            "每步完成后标记进度",
            "遇到问题立即记录"
        ]
    },
    {
        "id": 5,
        "name": "tdd",
        "display_name": "测试驱动",
        "description": "RED-GREEN-REFACTOR循环",
        "hard_gate": True,
        "checklist": [
            "先写失败的测试（RED）",
            "写最少代码让测试通过（GREEN）",
            "重构代码保持测试通过（REFACTOR）",
            "如果缺少测试数据，停下来要mock data"
        ]
    },
    {
        "id": 6,
        "name": "code_review",
        "display_name": "双重审查",
        "description": "自审 + AI审查",
        "hard_gate": True,
        "checklist": [
            "开发者自审代码",
            "AI进行安全审查",
            "AI进行性能审查",
            "修复所有严重问题"
        ]
    },
    {
        "id": 7,
        "name": "completion",
        "display_name": "完成合并",
        "description": "确认所有测试通过，合并分支",
        "hard_gate": True,
        "checklist": [
            "所有测试通过",
            "代码覆盖率达标",
            "git diff干净无噪音",
            "合并到主分支"
        ]
    }
]


class SuperPowersSession:
    """
    Super Powers会话

    管理单个开发任务的7阶段强制工作流
    """

    def __init__(self, project_name: str, description: str = ""):
        self.session_id = f"sp_{int(datetime.now().timestamp())}"
        self.project_name = project_name
        self.description = description
        self.current_stage = 1
        self.completed_stages: List[int] = []
        self.stage_results: Dict[int, Dict] = {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.status = "active"  # active, completed, blocked

    def get_current_stage_info(self) -> Dict[str, Any]:
        """获取当前阶段信息"""
        for stage in STAGES:
            if stage["id"] == self.current_stage:
                return stage
        return STAGES[-1]

    def advance(self, stage_result: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        推进到下一阶段

        如果当前阶段有hard_gate，必须先通过检查
        """
        current = self.get_current_stage_info()

        # 检查硬门禁
        if current["hard_gate"] and stage_result:
            checklist = current.get("checklist", [])
            completed = stage_result.get("checklist_completed", [])
            missing = [item for item in checklist if item not in completed]

            if missing:
                return {
                    "success": False,
                    "blocked": True,
                    "stage": current["name"],
                    "message": f"硬门禁未通过，缺少: {missing}",
                    "missing_items": missing
                }

        # 记录当前阶段结果
        self.completed_stages.append(self.current_stage)
        if stage_result:
            self.stage_results[self.current_stage] = stage_result

        # 推进到下一阶段
        if self.current_stage < len(STAGES):
            self.current_stage += 1
            self.updated_at = datetime.now()

            if self.current_stage > len(STAGES):
                self.status = "completed"

            return {
                "success": True,
                "advanced_to": self.get_current_stage_info()["name"],
                "session_id": self.session_id
            }
        else:
            self.status = "completed"
            return {
                "success": True,
                "message": "所有阶段已完成！",
                "session_id": self.session_id
            }

    def get_progress(self) -> Dict[str, Any]:
        """获取进度"""
        total = len(STAGES)
        completed = len(self.completed_stages)
        return {
            "session_id": self.session_id,
            "project": self.project_name,
            "status": self.status,
            "current_stage": self.current_stage,
            "current_stage_name": self.get_current_stage_info()["display_name"],
            "completed_stages": completed,
            "total_stages": total,
            "progress_percent": round(completed / total * 100, 1),
            "stages_detail": [
                {
                    "id": s["id"],
                    "name": s["display_name"],
                    "status": "completed" if s["id"] in self.completed_stages
                    else ("current" if s["id"] == self.current_stage else "pending"),
                    "hard_gate": s["hard_gate"]
                }
                for s in STAGES
            ]
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "project_name": self.project_name,
            "description": self.description,
            "current_stage": self.current_stage,
            "completed_stages": self.completed_stages,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class SuperPowersEngine:
    """
    Super Powers引擎

    管理多个开发会话，提供统一的工作流控制
    """

    def __init__(self):
        self.sessions: Dict[str, SuperPowersSession] = {}

    def create_session(self, project_name: str, description: str = "") -> SuperPowersSession:
        """创建新会话"""
        session = SuperPowersSession(project_name, description)
        self.sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[SuperPowersSession]:
        """获取会话"""
        return self.sessions.get(session_id)

    def list_sessions(self) -> List[Dict[str, Any]]:
        """列出所有会话"""
        return [s.to_dict() for s in self.sessions.values()]

    def get_all_stages(self) -> List[Dict[str, Any]]:
        """获取所有阶段定义"""
        return STAGES


# ============================================================
# 演示
# ============================================================

def main():
    print("=" * 60)
    print("  Super Powers Engine - AI编程纪律引擎")
    print("=" * 60)

    engine = SuperPowersEngine()

    # 创建会话
    session = engine.create_session("用户权限管理系统", "实现RBAC权限控制")
    print(f"\n[✓] 创建会话: {session.project_name} (ID: {session.session_id})")

    # 展示7阶段工作流
    print("\n7阶段强制工作流:")
    for stage in STAGES:
        gate = " [硬门禁]" if stage["hard_gate"] else ""
        print(f"  {stage['id']}. {stage['display_name']} - {stage['description']}{gate}")

    # 模拟推进
    print("\n--- 模拟执行 ---")

    # 阶段1: 脑暴
    result = session.advance({
        "checklist_completed": [
            "明确功能需求和边界",
            "识别技术风险和依赖",
            "定义验收标准",
            "确认范围不蔓延"
        ]
    })
    print(f"脑暴阶段: {result}")

    # 阶段2: Git隔离
    result = session.advance({
        "checklist_completed": [
            "创建git worktree",
            "确认基础分支干净",
            "验证CI环境可用"
        ]
    })
    print(f"Git隔离: {result}")

    # 查看进度
    progress = session.get_progress()
    print(f"\n当前进度: {progress['progress_percent']}%")
    print(f"当前阶段: {progress['current_stage_name']}")

    print("\n[FORCE VALIDATION] 这是硬门禁，不允许跳过！")
    print("示例: Agent写完代码 → 自动进入TDD阶段")
    print("→ 如果缺少测试数据，Agent停下来要求提供mock data")
    print("→ 这在裸跑Claude Code中是不可能的！")


if __name__ == "__main__":
    main()
