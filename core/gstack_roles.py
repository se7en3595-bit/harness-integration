#!/usr/bin/env python3
"""
AI Agent Harness - G-Stack 多角色决策系统（第三层）

基于Gyro的G-Stack理念：23个专家角色并行决策，不是AI自己审自己
多视角审查确保决策质量，避免单一视角盲区

核心理念：
- 不要一次用所有23角色！按需选择2-4个最相关的角色
- 每个角色有独立的评分标准和关注点
- Office Hours模式：多角色并行讨论，形成共识
- 角色不是越多越好，关键是选对角色

角色分类：
- Product: CEO, PM, UX Designer, Data Analyst
- Engineering: Tech Lead, Senior Dev, Junior Dev, Architect
- Security: Security Architect, Security Engineer
- Operations: DevOps, SRE, QA Lead
- Business: Sales, Marketing, Support
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional


# ============================================================
# 23个专家角色定义
# ============================================================

ROLES = {
    # Product
    "ceo": {
        "name": "CEO",
        "category": "product",
        "focus": ["战略对齐", "商业价值", "优先级排序"],
        "scoring_criteria": ["ROI", "市场契合度", "竞争优势"]
    },
    "pm": {
        "name": "产品经理",
        "category": "product",
        "focus": ["用户需求", "功能范围", "交付时间"],
        "scoring_criteria": ["用户价值", "需求完整性", "可行性"]
    },
    "ux_designer": {
        "name": "UX设计师",
        "category": "product",
        "focus": ["用户体验", "交互设计", "可用性"],
        "scoring_criteria": ["易用性", "一致性", "无障碍性"]
    },
    "data_analyst": {
        "name": "数据分析师",
        "category": "product",
        "focus": ["数据驱动", "指标定义", "效果评估"],
        "scoring_criteria": ["可量化", "可追踪", "可验证"]
    },
    # Engineering
    "tech_lead": {
        "name": "技术负责人",
        "category": "engineering",
        "focus": ["技术方案", "架构设计", "代码质量"],
        "scoring_criteria": ["技术可行性", "架构合理性", "可维护性"]
    },
    "senior_dev": {
        "name": "高级开发",
        "category": "engineering",
        "focus": ["实现细节", "性能优化", "最佳实践"],
        "scoring_criteria": ["代码质量", "性能", "可扩展性"]
    },
    "junior_dev": {
        "name": "初级开发",
        "category": "engineering",
        "focus": ["学习成本", "实现难度", "文档完整性"],
        "scoring_criteria": ["可读性", "文档化", "学习曲线"]
    },
    "architect": {
        "name": "架构师",
        "category": "engineering",
        "focus": ["系统架构", "技术选型", "长期演进"],
        "scoring_criteria": ["架构合理性", "技术前瞻性", "成本控制"]
    },
    # Security
    "security_architect": {
        "name": "安全架构师",
        "category": "security",
        "focus": ["安全风险评估", "合规要求", "威胁建模"],
        "scoring_criteria": ["安全性", "合规性", "风险可控"]
    },
    "security_engineer": {
        "name": "安全工程师",
        "category": "security",
        "focus": ["漏洞检测", "渗透测试", "安全加固"],
        "scoring_criteria": ["漏洞数量", "修复覆盖率", "安全测试"]
    },
    # Operations
    "devops": {
        "name": "DevOps工程师",
        "category": "operations",
        "focus": ["CI/CD", "部署流程", "环境管理"],
        "scoring_criteria": ["部署效率", "回滚能力", "环境一致性"]
    },
    "sre": {
        "name": "SRE工程师",
        "category": "operations",
        "focus": ["系统可靠性", "监控告警", "故障恢复"],
        "scoring_criteria": ["SLA达标率", "MTTR", "监控覆盖率"]
    },
    "qa_lead": {
        "name": "QA负责人",
        "category": "operations",
        "focus": ["测试策略", "质量保障", "缺陷管理"],
        "scoring_criteria": ["测试覆盖率", "缺陷密度", "回归测试"]
    },
    # Business
    "sales_lead": {
        "name": "销售负责人",
        "category": "business",
        "focus": ["客户需求", "竞品分析", "定价策略"],
        "scoring_criteria": ["客户满意度", "竞争力", "收入影响"]
    },
    "marketing": {
        "name": "市场营销",
        "category": "business",
        "focus": ["品牌影响", "用户获取", "市场定位"],
        "scoring_criteria": ["品牌一致性", "获客成本", "市场影响"]
    },
    "support": {
        "name": "客户支持",
        "category": "business",
        "focus": ["客户反馈", "问题解决", "用户满意度"],
        "scoring_criteria": ["支持成本", "解决率", "客户满意度"]
    },
}

# 补充到23个角色
ROLES.update({
    "backend_dev": {"name": "后端开发", "category": "engineering", "focus": ["API设计", "数据库", "服务架构"], "scoring_criteria": ["API规范", "数据一致性", "服务稳定性"]},
    "frontend_dev": {"name": "前端开发", "category": "engineering", "focus": ["UI实现", "性能优化", "兼容性"], "scoring_criteria": ["渲染性能", "兼容性", "代码质量"]},
    "data_engineer": {"name": "数据工程师", "category": "engineering", "focus": ["数据管道", "ETL", "数据质量"], "scoring_criteria": ["数据准确性", "管道稳定性", "处理效率"]},
    "ml_engineer": {"name": "ML工程师", "category": "engineering", "focus": ["模型训练", "特征工程", "模型部署"], "scoring_criteria": ["模型性能", "训练效率", "部署稳定性"]},
    "product_designer": {"name": "产品设计师", "category": "product", "focus": ["产品设计", "原型制作", "用户研究"], "scoring_criteria": ["设计一致性", "用户反馈", "迭代速度"]},
    "technical_writer": {"name": "技术文档", "category": "engineering", "focus": ["文档质量", "API文档", "用户指南"], "scoring_criteria": ["文档完整性", "准确性", "可读性"]},
    "compliance": {"name": "合规官", "category": "security", "focus": ["法规合规", "数据隐私", "审计"], "scoring_criteria": ["合规覆盖率", "隐私保护", "审计通过率"]},
    "project_manager": {"name": "项目经理", "category": "operations", "focus": ["进度管理", "资源协调", "风险管理"], "scoring_criteria": ["进度达标率", "资源利用率", "风险可控性"]},
})


class RoleReview:
    """单个角色的审查结果"""

    def __init__(self, role_id: str, role_def: Dict[str, Any]):
        self.role_id = role_id
        self.role_name = role_def["name"]
        self.category = role_def["category"]
        self.score = 0.0
        self.feedback: List[str] = []
        self.concerns: List[str] = []
        self.recommendations: List[str] = []
        self.reviewed_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role_name,
            "category": self.category,
            "score": round(self.score, 3),
            "feedback": self.feedback,
            "concerns": self.concerns,
            "recommendations": self.recommendations
        }


class OfficeHours:
    """
    办公室会议

    多角色并行讨论，形成共识决策
    """

    def __init__(self, topic: str, participants: List[str]):
        self.topic = topic
        self.participants = participants
        self.reviews: List[RoleReview] = []
        self.consensus_score = 0.0
        self.decision_points: List[str] = []
        self.created_at = datetime.now()
        self.status = "pending"  # pending, in_progress, completed

    def conduct(self, content: str = "") -> Dict[str, Any]:
        """
        执行办公室会议

        每个参与者独立审查，然后汇总共识
        """
        self.status = "in_progress"
        self.reviews = []

        for role_id in self.participants:
            role_def = ROLES.get(role_id)
            if not role_def:
                continue

            review = self._review_as_role(role_id, role_def, content)
            self.reviews.append(review)

        # 计算共识分数
        if self.reviews:
            self.consensus_score = sum(r.score for r in self.reviews) / len(self.reviews)

        # 生成决策要点
        self.decision_points = self._generate_decisions()

        self.status = "completed"

        return {
            "topic": self.topic,
            "participants": self.participants,
            "consensus_score": round(self.consensus_score, 3),
            "reviews": [r.to_dict() for r in self.reviews],
            "decision_points": self.decision_points,
            "status": self.status
        }

    def _review_as_role(self, role_id: str, role_def: Dict[str, Any], content: str) -> RoleReview:
        """
        以特定角色视角审查内容。

        评分逻辑：检查 content 中是否覆盖了该角色的关注点和评分标准。
        每个关注点命中 +1 分，每个评分标准命中 +1 分，
        最终归一化到 [0.5, 1.0] 区间。
        没有内容时给中性分 0.6。
        """
        review = RoleReview(role_id, role_def)
        focus_areas = role_def["focus"]
        scoring_criteria = role_def["scoring_criteria"]

        if not content.strip():
            review.score = 0.6
            review.feedback = [f"未提供内容，无法评估{focus}" for focus in focus_areas[:2]]
            review.concerns = ["内容为空，建议补充具体方案描述"]
            return review

        content_lower = content.lower()

        # 关注点命中检测：把每个关注点拆成关键词，检查是否出现在内容中
        focus_hits = []
        focus_misses = []
        for focus in focus_areas:
            # 拆分关注点为词（中文按字符，英文按空格）
            keywords = [w for w in focus.replace("、", " ").replace("/", " ").split() if len(w) > 1]
            hit = any(kw.lower() in content_lower for kw in keywords) if keywords else False
            if hit:
                focus_hits.append(focus)
            else:
                focus_misses.append(focus)

        # 评分标准命中检测
        criteria_hits = []
        criteria_misses = []
        for criterion in scoring_criteria:
            keywords = [w for w in criterion.replace("、", " ").replace("/", " ").split() if len(w) > 1]
            hit = any(kw.lower() in content_lower for kw in keywords) if keywords else False
            if hit:
                criteria_hits.append(criterion)
            else:
                criteria_misses.append(criterion)

        # 计算分数：命中率映射到 [0.5, 1.0]
        total_checks = len(focus_areas) + len(scoring_criteria)
        total_hits = len(focus_hits) + len(criteria_hits)
        hit_rate = total_hits / total_checks if total_checks > 0 else 0.0
        review.score = 0.5 + hit_rate * 0.5

        # 生成有意义的反馈
        if focus_hits:
            review.feedback = [f"内容覆盖了「{f}」" for f in focus_hits]
        else:
            review.feedback = [f"内容未提及{role_def['name']}关注的任何方面"]

        if criteria_misses:
            review.recommendations = [f"建议补充「{c}」相关内容" for c in criteria_misses[:2]]

        if focus_misses:
            review.concerns = [f"缺少对「{f}」的说明" for f in focus_misses[:2]]

        return review

    def _generate_decisions(self) -> List[str]:
        """基于所有审查生成决策要点"""
        decisions = []
        all_concerns = []
        all_recommendations = []

        for review in self.reviews:
            all_concerns.extend(review.concerns)
            all_recommendations.extend(review.recommendations)

        if self.consensus_score >= 0.85:
            decisions.append("高共识度，建议推进")
        elif self.consensus_score >= 0.7:
            decisions.append("中等共识，建议解决担忧后推进")
        else:
            decisions.append("共识度低，建议重新讨论")

        if all_concerns:
            decisions.append(f"需要关注的问题: {len(all_concerns)}个")

        decisions.extend(all_recommendations[:3])

        return decisions


class GStackEngine:
    """
    G-Stack引擎

    管理角色审查和办公室会议
    """

    def __init__(self):
        self.office_hours_history: List[Dict] = []

    def get_all_roles(self) -> Dict[str, Dict[str, Any]]:
        """获取所有角色定义"""
        return ROLES

    def get_roles_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """按分类获取角色"""
        return {k: v for k, v in ROLES.items() if v["category"] == category}

    def recommend_roles(self, topic: str) -> List[str]:
        """
        根据讨论主题推荐角色

        不要一次用所有23角色！按需选择2-4个最相关的
        """
        topic_lower = topic.lower()
        recommendations = []

        # 安全相关
        if any(kw in topic_lower for kw in ["安全", "权限", "认证", "加密", "security", "auth"]):
            recommendations.extend(["security_architect", "tech_lead"])

        # 产品相关
        if any(kw in topic_lower for kw in ["功能", "需求", "用户", "feature", "product"]):
            recommendations.extend(["pm", "ux_designer"])

        # 技术相关
        if any(kw in topic_lower for kw in ["架构", "设计", "技术", "api", "database"]):
            recommendations.extend(["architect", "tech_lead"])

        # 商业相关
        if any(kw in topic_lower for kw in ["商业", "收入", "市场", "sales", "revenue"]):
            recommendations.extend(["ceo", "sales_lead"])

        # 默认推荐
        if not recommendations:
            recommendations = ["tech_lead", "pm"]

        return list(dict.fromkeys(recommendations))[:4]  # 去重，最多4个

    def conduct_office_hours(self, topic: str, participants: List[str],
                              content: str = "") -> Dict[str, Any]:
        """
        召集办公室会议

        多角色并行讨论，形成共识决策
        """
        office_hours = OfficeHours(topic, participants)
        result = office_hours.conduct(content)

        self.office_hours_history.append({
            "topic": topic,
            "participants": participants,
            "consensus_score": result["consensus_score"],
            "timestamp": datetime.now().isoformat()
        })

        return result

    def get_history(self) -> List[Dict[str, Any]]:
        """获取会议历史"""
        return self.office_hours_history


# ============================================================
# 演示
# ============================================================

def main():
    print("=" * 60)
    print("  G-Stack Roles - 多角色决策系统")
    print("=" * 60)

    engine = GStackEngine()

    # 展示角色分类
    print(f"\n共{len(ROLES)}个专家角色:")
    categories = {}
    for role_id, role_def in ROLES.items():
        cat = role_def["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(role_def["name"])

    for cat, roles in categories.items():
        print(f"  [{cat}] {', '.join(roles)}")

    # 角色推荐
    topic = "API权限系统设计"
    recommended = engine.recommend_roles(topic)
    print(f"\n主题 '{topic}' 推荐角色: {recommended}")

    # 办公室会议
    print(f"\n--- Office Hours: {topic} ---")
    result = engine.conduct_office_hours(
        topic=topic,
        participants=["ceo", "pm", "tech_lead", "security_architect"],
        content="设计一个新的API权限控制系统"
    )

    print(f"参与者: {result['participants']}")
    print(f"共识评分: {result['consensus_score']:.1%}")
    print("\n各角色评分:")
    for review in result["reviews"]:
        print(f"  [{review['role']}] {review['score']:.1%}")
        if review["concerns"]:
            print(f"    担忧: {review['concerns']}")

    print(f"\n决策要点:")
    for point in result["decision_points"]:
        print(f"  - {point}")

    print("\n[关键洞察] 不要一次用所有23个角色！")
    print("按需选择2-4个最相关的角色：")
    print("  - /plan-ceo-review → 战略对齐")
    print("  - /qa → 测试验证")
    print("  - /cso → 安全风险评估")


if __name__ == "__main__":
    main()
