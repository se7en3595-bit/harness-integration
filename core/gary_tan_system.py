#!/usr/bin/env python3
"""
AI Agent Harness - Gar Tan三层复利系统

基于Gar Tan的个人复利系统理念：
- 薄壳层(Thin Shell)：只做路由的轻量调度器
- 厚技能层(Skillify)：自动生成和优化的技能库
- 厚数据层(Brain Page)：结构化知识图谱和持续积累

核心理念：
- 竞争优势 = 模型引擎 + 技能文件 + 数据积累 + 关系网络
- 知识复利：每次学习都让下一次更快更准
- 薄壳调度：调度器只路由，不塞业务逻辑
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional


# ============================================================
# 薄壳调度层
# ============================================================

class ThinShellScheduler:
    """
    薄壳调度层 - 只做路由的轻量调度器

    核心原则：
    - 调度器不包含业务逻辑
    - 只负责将请求路由到正确的技能
    - 保持轻量，避免上下文污染
    """

    def __init__(self):
        self.skill_registry: Dict[str, Dict[str, Any]] = {}
        self.route_history: List[Dict] = []

    def register_skill(self, skill_name: str, handler: Any, description: str = "",
                       category: str = "general"):
        """注册技能"""
        self.skill_registry[skill_name] = {
            "handler": handler,
            "description": description,
            "category": category,
            "registered_at": datetime.now().isoformat(),
            "use_count": 0
        }

    def route_request(self, user_input: str, context: Dict = None) -> Dict[str, Any]:
        """
        路由用户请求到合适的技能

        基于关键词匹配和上下文分析
        """
        context = context or {}
        input_lower = user_input.lower()

        # 关键词路由表
        route_map = {
            "book_mirror": ["mirror", "book", "书籍", "镜像", "read", "读书"],
            "meeting_analyzer": ["meeting", "会议", "讨论", "讨论记录", "会议纪要"],
            "knowledge_query": ["knowledge", "知识", "查询", "搜索", "find"],
            "skill_create": ["skill", "技能", "创建", "生成", "自动化"],
            "brain_page": ["brain", "page", "脑图", "页面", "笔记"],
        }

        # 匹配最佳技能
        best_match = None
        best_score = 0

        for skill_name, keywords in route_map.items():
            score = sum(1 for kw in keywords if kw in input_lower)
            if score > best_score:
                best_score = score
                best_match = skill_name

        # 默认处理器
        if not best_match or best_score == 0:
            best_match = "universal_processor"

        # 记录路由历史
        route_record = {
            "input": user_input[:100],
            "routed_to": best_match,
            "score": best_score,
            "timestamp": datetime.now().isoformat()
        }
        self.route_history.append(route_record)

        # 更新使用计数
        if best_match in self.skill_registry:
            self.skill_registry[best_match]["use_count"] += 1

        return {
            "skill": best_match,
            "confidence": min(best_score / 3, 1.0),
            "context": context
        }

    def get_registry_stats(self) -> Dict[str, Any]:
        """获取注册表统计"""
        return {
            "total_skills": len(self.skill_registry),
            "skills": {
                name: {
                    "description": info["description"],
                    "category": info["category"],
                    "use_count": info["use_count"]
                }
                for name, info in self.skill_registry.items()
            },
            "total_routes": len(self.route_history),
            "recent_routes": self.route_history[-5:]
        }


# ============================================================
# Skillify引擎
# ============================================================

class SkillifyEngine:
    """
    Skillify引擎 - 自动生成和优化技能

    核心流程：
    1. 观察用户手动操作
    2. 提取可复用模式
    3. 自动生成技能
    4. 持续优化技能

    演进路径：手动操作 → 技能模板 → 自动优化
    """

    def __init__(self):
        self.skill_templates: Dict[str, Dict] = {}
        self.optimization_history: List[Dict] = []
        self.pattern_library: Dict[str, List[str]] = {}

    def observe_action(self, action_description: str, steps: List[str],
                       result: Any = None) -> Dict[str, Any]:
        """
        观察用户动作，提取可复用模式
        """
        # 提取模式签名
        pattern_sig = self._extract_pattern_signature(steps)

        # 检查是否已有相似模板
        similar = self._find_similar_template(pattern_sig)

        if similar:
            # 优化现有模板
            optimized = self._optimize_template(similar, steps, result)
            return {
                "action": "optimized",
                "template_id": optimized["template_id"],
                "improvement": optimized["improvement"]
            }
        else:
            # 创建新模板
            template = self._create_template(action_description, steps, result)
            return {
                "action": "created",
                "template_id": template["template_id"],
                "skill_name": template["name"]
            }

    def process_user_action(self, action_description: str,
                            result_data: Any = None) -> Dict[str, Any]:
        """
        处理用户动作并生成技能

        这是Skillify的核心入口
        """
        # 提取可复用模式
        patterns = self._extract_patterns(action_description)

        # 生成技能定义
        skill_def = self._generate_skill_definition(action_description, patterns)

        # 注册技能
        self.skill_templates[skill_def["id"]] = skill_def

        # 记录优化历史
        self.optimization_history.append({
            "action": action_description,
            "skill_generated": skill_def["id"],
            "patterns_found": len(patterns),
            "timestamp": datetime.now().isoformat()
        })

        return {
            "success": True,
            "skill_id": skill_def["id"],
            "skill_name": skill_def["name"],
            "patterns_extracted": len(patterns),
            "auto_optimized": True
        }

    def auto_optimize(self, skill_id: str, usage_data: Dict) -> Dict[str, Any]:
        """
        基于使用数据自动优化技能
        """
        if skill_id not in self.skill_templates:
            return {"error": f"Skill {skill_id} not found"}

        template = self.skill_templates[skill_id]

        # 分析使用模式
        success_rate = usage_data.get("success_rate", 0)
        avg_duration = usage_data.get("avg_duration", 0)
        common_errors = usage_data.get("common_errors", [])

        optimizations = []

        if success_rate < 0.8:
            optimizations.append("增加错误处理步骤")

        if avg_duration > 300:  # 超过5分钟
            optimizations.append("优化执行步骤，减少冗余操作")

        for error in common_errors:
            optimizations.append(f"修复常见错误: {error}")

        # 应用优化
        template["optimizations"] = optimizations
        template["last_optimized"] = datetime.now().isoformat()
        template["version"] = template.get("version", 1) + 1

        return {
            "skill_id": skill_id,
            "optimizations_applied": len(optimizations),
            "new_version": template["version"]
        }

    def get_skill_library(self) -> Dict[str, Any]:
        """获取技能库"""
        return {
            "total_skills": len(self.skill_templates),
            "skills": {
                sid: {
                    "name": s["name"],
                    "version": s.get("version", 1),
                    "patterns": len(s.get("patterns", [])),
                    "last_optimized": s.get("last_optimized", "never")
                }
                for sid, s in self.skill_templates.items()
            },
            "total_optimizations": len(self.optimization_history)
        }

    def _extract_pattern_signature(self, steps: List[str]) -> str:
        """提取模式签名"""
        key_actions = []
        for step in steps:
            words = step.lower().split()
            key_actions.extend(words[:3])
        return "_".join(key_actions[:10])

    def _find_similar_template(self, pattern_sig: str) -> Optional[Dict]:
        """查找相似模板"""
        for tid, template in self.skill_templates.items():
            if self._calc_similarity(pattern_sig, template.get("signature", "")) > 0.7:
                return {"template_id": tid, **template}
        return None

    def _calc_similarity(self, sig1: str, sig2: str) -> float:
        """计算相似度"""
        set1 = set(sig1.split("_"))
        set2 = set(sig2.split("_"))
        if not set1 or not set2:
            return 0.0
        return len(set1 & set2) / len(set1 | set2)

    def _optimize_template(self, existing: Dict, new_steps: List[str],
                           result: Any) -> Dict:
        """优化现有模板"""
        template = self.skill_templates[existing["template_id"]]
        template["steps"] = list(set(template.get("steps", []) + new_steps))
        template["last_optimized"] = datetime.now().isoformat()
        return {
            "template_id": existing["template_id"],
            "improvement": f"新增 {len(new_steps)} 个步骤"
        }

    def _create_template(self, description: str, steps: List[str],
                         result: Any) -> Dict:
        """创建新模板"""
        template_id = f"skill_{hashlib.md5(description.encode()).hexdigest()[:8]}"
        return {
            "template_id": template_id,
            "name": description[:50],
            "steps": steps,
            "signature": self._extract_pattern_signature(steps),
            "patterns": self._extract_patterns(description),
            "created_at": datetime.now().isoformat(),
            "version": 1
        }

    def _extract_patterns(self, text: str) -> List[str]:
        """提取模式"""
        patterns = []
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if len(line) > 5 and len(line) < 200:
                patterns.append(line)
        return patterns[:10]

    def _generate_skill_definition(self, description: str,
                                   patterns: List[str]) -> Dict:
        """生成技能定义"""
        skill_id = f"skill_{hashlib.md5(description.encode()).hexdigest()[:8]}"
        return {
            "id": skill_id,
            "name": description[:50],
            "description": description,
            "patterns": patterns,
            "created_at": datetime.now().isoformat(),
            "version": 1
        }


# ============================================================
# Brain Page数据层
# ============================================================

class BrainPage:
    """
    Brain Page - 个人知识库页面

    每个Brain Page代表一个知识实体（书籍、会议、项目等）
    包含时间线事件、交叉引用和持续更新
    """

    def __init__(self, page_id: str, name: str, page_type: str = "general"):
        self.page_id = page_id
        self.name = name
        self.page_type = page_type  # book, meeting, project, concept
        self.content: str = ""
        self.timeline_events: List[Dict] = []
        self.cross_references: List[str] = []  # 关联的其他page_id
        self.tags: List[str] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.version = 1

    def update(self, new_content: str, event_type: str = "update"):
        """更新页面内容"""
        self.content = new_content
        self.timeline_events.append({
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "content_preview": new_content[:100]
        })
        self.updated_at = datetime.now()
        self.version += 1

    def add_cross_reference(self, target_page_id: str, relation: str = "related"):
        """添加交叉引用"""
        ref = {"page_id": target_page_id, "relation": relation}
        if ref not in self.cross_references:
            self.cross_references.append(target_page_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_id": self.page_id,
            "name": self.name,
            "type": self.page_type,
            "content_length": len(self.content),
            "timeline_events": len(self.timeline_events),
            "cross_references": len(self.cross_references),
            "tags": self.tags,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class BrainDataManager:
    """
    厚数据层管理器 - Brain Page系统

    管理所有Brain Page，提供知识图谱功能
    """

    def __init__(self):
        self.brain_pages: Dict[str, BrainPage] = {}
        self.knowledge_density = 0.0
        self.entity_index: Dict[str, List[str]] = {}  # entity_name -> [page_ids]

    def create_or_update_page(self, entity_name: str, entity_type: str,
                              content: str, tags: List[str] = None) -> str:
        """创建或更新Brain Page"""
        page_id = f"page_{entity_name.lower().replace(' ', '_')}"

        if page_id in self.brain_pages:
            page = self.brain_pages[page_id]
            page.update(content, event_type="update")
        else:
            page = BrainPage(page_id, entity_name, entity_type)
            page.content = content
            page.tags = tags or []
            self.brain_pages[page_id] = page

        # 更新实体索引
        if entity_name not in self.entity_index:
            self.entity_index[entity_name] = []
        if page_id not in self.entity_index[entity_name]:
            self.entity_index[entity_name].append(page_id)

        # 重新计算知识密度
        self._recalculate_density()

        return page_id

    def get_page(self, page_id: str) -> Optional[BrainPage]:
        """获取Brain Page"""
        return self.brain_pages.get(page_id)

    def search_pages(self, query: str) -> List[Dict[str, Any]]:
        """搜索Brain Page"""
        results = []
        query_lower = query.lower()

        for page_id, page in self.brain_pages.items():
            score = 0
            if query_lower in page.name.lower():
                score += 3
            if query_lower in page.content.lower():
                score += 1
            if any(query_lower in tag.lower() for tag in page.tags):
                score += 2

            if score > 0:
                results.append({
                    "page_id": page_id,
                    "name": page.name,
                    "type": page.page_type,
                    "score": score,
                    "preview": page.content[:100]
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def get_knowledge_dashboard(self) -> Dict[str, Any]:
        """获取知识图谱仪表板"""
        total_pages = len(self.brain_pages)
        total_events = sum(len(p.timeline_events) for p in self.brain_pages.values())
        total_refs = sum(len(p.cross_references) for p in self.brain_pages.values())

        # 按类型统计
        type_stats = {}
        for page in self.brain_pages.values():
            t = page.page_type
            if t not in type_stats:
                type_stats[t] = 0
            type_stats[t] += 1

        return {
            "total_pages": total_pages,
            "total_timeline_events": total_events,
            "total_cross_references": total_refs,
            "knowledge_density": self.knowledge_density,
            "by_type": type_stats,
            "recent_pages": sorted(
                [p.to_dict() for p in self.brain_pages.values()],
                key=lambda x: x["updated_at"],
                reverse=True
            )[:5]
        }

    def _recalculate_density(self):
        """重新计算知识密度"""
        total_pages = len(self.brain_pages)
        if total_pages == 0:
            self.knowledge_density = 0.0
            return

        total_events = sum(len(p.timeline_events) for p in self.brain_pages.values())
        total_refs = sum(len(p.cross_references) for p in self.brain_pages.values())

        # 密度 = (事件数 + 引用数 * 2) / 页面数
        self.knowledge_density = round(
            (total_events + total_refs * 2) / total_pages, 2
        )


# ============================================================
# Gar Tan三层复利系统主类
# ============================================================

class GarTanSystem:
    """
    Gar Tan三层复利系统主类

    整合薄壳调度、Skillify生成和Brain Page积累

    竞争优势公式：
    护城河 = 模型引擎 + 技能文件 + 数据积累 + 关系网络
    """

    def __init__(self):
        self.thin_shell = ThinShellScheduler()
        self.skillify_engine = SkillifyEngine()
        self.brain_manager = BrainDataManager()

        # 注册内置技能
        self._register_builtin_skills()

    def _register_builtin_skills(self):
        """注册内置技能"""
        self.thin_shell.register_skill(
            "book_mirror", self.mirror_book,
            "将书籍内容映射到个人脑图", "learning"
        )
        self.thin_shell.register_skill(
            "meeting_analyzer", self.analyze_meeting,
            "分析会议记录并提取洞察", "productivity"
        )
        self.thin_shell.register_skill(
            "knowledge_query", self.query_knowledge,
            "查询个人知识库", "learning"
        )

    def mirror_book(self, book_title: str, book_content: str) -> Dict[str, Any]:
        """
        镜像书籍到个人脑图

        流程：章节提取 → 概念映射 → 脑图更新 → 技能生成
        """
        # 1. 提取章节
        chapters = self._extract_chapters(book_content)

        # 2. 提取概念并映射
        all_concepts = []
        for chapter in chapters:
            concepts = self._extract_concepts(chapter["content"])
            all_concepts.extend(concepts)

        # 3. 更新Brain Page
        book_page_id = self.brain_manager.create_or_update_page(
            entity_name=book_title,
            entity_type="book",
            content=book_content[:500],
            tags=["book", "brain_page", "learning"]
        )

        # 4. 为每个章节创建子页面
        for chapter in chapters:
            chapter_page_id = self.brain_manager.create_or_update_page(
                entity_name=f"{book_title} - {chapter['title']}",
                entity_type="chapter",
                content=chapter["content"][:300],
                tags=["chapter", book_title.lower().replace(" ", "_")]
            )
            # 添加交叉引用
            book_page = self.brain_manager.get_page(book_page_id)
            if book_page:
                book_page.add_cross_reference(chapter_page_id, "contains")

        # 5. 触发Skillify生成
        skill_result = self.skillify_engine.process_user_action(
            f"mirror book: {book_title}",
            {"chapters": len(chapters), "concepts": len(all_concepts)}
        )

        # 6. 计算知识密度
        density = self.brain_manager.knowledge_density

        return {
            "success": True,
            "book_page_id": book_page_id,
            "chapters_processed": len(chapters),
            "concepts_mapped": len(all_concepts),
            "skill_generated": skill_result["success"],
            "skill_id": skill_result.get("skill_id", ""),
            "knowledge_density": density,
            "completion_time": f"{len(chapters) * 5} minutes"
        }

    def analyze_meeting(self, transcript: str,
                        participants: List[str] = None) -> Dict[str, Any]:
        """
        分析会议记录

        提取决策、行动项和关键讨论点
        """
        participants = participants or []

        # 提取决策
        decisions = self._extract_by_keywords(
            transcript,
            ["decide", "agree", "approve", "choose", "confirm",
             "决定", "同意", "确认", "通过"]
        )

        # 提取行动项
        actions = self._extract_by_keywords(
            transcript,
            ["action", "todo", "follow up", "will do", "responsible",
             "负责", "跟进", "待办", "行动"]
        )

        # 提取关键讨论
        discussions = self._extract_by_keywords(
            transcript,
            ["discuss", "consider", "review", "propose", "suggest",
             "建议", "讨论", "考虑", "提出"]
        )

        # 创建会议Brain Page
        meeting_page_id = self.brain_manager.create_or_update_page(
            entity_name=f"Meeting {datetime.now().strftime('%Y-%m-%d')}",
            entity_type="meeting",
            content=transcript[:500],
            tags=["meeting", "decision"] + [p.lower() for p in participants]
        )

        # 为每个参与者更新页面
        for participant in participants:
            participant_page_id = self.brain_manager.create_or_update_page(
                entity_name=participant,
                entity_type="person",
                content=f"Participated in meeting on {datetime.now().strftime('%Y-%m-%d')}",
                tags=["person", "meeting"]
            )
            # 添加交叉引用
            meeting_page = self.brain_manager.get_page(meeting_page_id)
            if meeting_page:
                meeting_page.add_cross_reference(participant_page_id, "participant")

        return {
            "success": True,
            "meeting_page_id": meeting_page_id,
            "decisions_captured": len(decisions),
            "action_items_extracted": len(actions),
            "discussions_noted": len(discussions),
            "participants_updated": len(participants),
            "decisions": decisions[:5],
            "action_items": actions[:5]
        }

    def query_knowledge(self, query: str) -> Dict[str, Any]:
        """查询个人知识库"""
        results = self.brain_manager.search_pages(query)
        dashboard = self.brain_manager.get_knowledge_dashboard()

        return {
            "query": query,
            "results": results,
            "total_matches": len(results),
            "knowledge_density": dashboard["knowledge_density"],
            "total_pages": dashboard["total_pages"]
        }

    def get_system_dashboard(self) -> Dict[str, Any]:
        """获取系统仪表板"""
        return {
            "thin_shell": self.thin_shell.get_registry_stats(),
            "skillify": self.skillify_engine.get_skill_library(),
            "brain_data": self.brain_manager.get_knowledge_dashboard(),
            "competitive_advantage": {
                "model_engine": "Active",
                "skill_files": len(self.skillify_engine.skill_templates),
                "data_accumulation": len(self.brain_manager.brain_pages),
                "relationship_network": sum(
                    len(p.cross_references)
                    for p in self.brain_manager.brain_pages.values()
                )
            },
            "formula": "护城河 = 模型引擎 + 技能文件 + 数据积累 + 关系网络"
        }

    def _extract_chapters(self, content: str) -> List[Dict]:
        """提取章节"""
        chapters = []
        lines = content.split('\n')
        current_chapter = {"index": 0, "title": "Introduction", "content": ""}
        chapter_index = 0

        for line in lines:
            if line.startswith('#'):
                if current_chapter["content"]:
                    chapters.append(current_chapter)
                chapter_index += 1
                current_chapter = {
                    "index": chapter_index,
                    "title": line.lstrip('#').strip(),
                    "content": ""
                }
            else:
                current_chapter["content"] += line + "\n"

        if current_chapter["content"]:
            chapters.append(current_chapter)

        return chapters if chapters else [
            {"index": 1, "title": "Full Content", "content": content}
        ]

    def _extract_concepts(self, content: str) -> List[str]:
        """提取概念"""
        concepts = []
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) > 10 and len(line) < 500:
                if not line.startswith('```') and not line.startswith('#'):
                    concepts.append(line)
        return concepts[:20]

    def _extract_by_keywords(self, text: str, keywords: List[str]) -> List[str]:
        """按关键词提取"""
        results = []
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if any(kw.lower() in line.lower() for kw in keywords) and len(line) > 5:
                results.append(line)
        return results[:10]


# ============================================================
# 演示
# ============================================================

def main():
    print("=" * 60)
    print("  Gar Tan Three-Layer Compounding System")
    print("=" * 60)

    system = GarTanSystem()

    print("\n三层架构:")
    print("  THIN SHELL (Router): 只做路由，不塞业务逻辑")
    print("  SKILLIFY (Auto-gen): 手工 → 技能 → 自动优化")
    print("  BRAIN DATA (Knowledge Graph): 结构化积累，指数级复利")

    print("\n[核心公式] 护城河 = 模型引擎 + 技能文件 + 数据积累 + 关系网络")

    # 案例1：镜像书籍
    print("\n--- 案例1: 书籍镜像 ---")
    book_content = """
# 第一章 面对困难
当事情分崩离析时，我们需要勇气面对...
# 第二章 在痛苦中找到平静
通过冥想和正念，我们可以在混乱中找到内心的平静...
# 第三章 与他人建立连接
真正的力量来自于与他人的真诚连接...
"""
    result = system.mirror_book("When Things Fall Apart", book_content)
    print(f"  书籍: {result['book_page_id']}")
    print(f"  章节数: {result['chapters_processed']}")
    print(f"  概念数: {result['concepts_mapped']}")
    print(f"  技能生成: {'成功' if result['skill_generated'] else '失败'}")
    print(f"  知识密度: {result['knowledge_density']}")

    # 案例2：会议分析
    print("\n--- 案例2: 会议分析 ---")
    meeting_transcript = """
    参会者: 张三, 李四, 王五
    讨论: 关于新产品功能的优先级排序
    决定: 优先开发用户登录功能
    行动项: 张三负责API设计，李四负责前端实现
    建议: 考虑使用JWT认证方案
    """
    result = system.analyze_meeting(meeting_transcript, ["张三", "李四", "王五"])
    print(f"  决策数: {result['decisions_captured']}")
    print(f"  行动项: {result['action_items_extracted']}")
    print(f"  参与者更新: {result['participants_updated']}")

    # 系统仪表板
    print("\n--- 系统仪表板 ---")
    dashboard = system.get_system_dashboard()
    print(f"  注册技能数: {dashboard['thin_shell']['total_skills']}")
    print(f"  Brain Pages: {dashboard['brain_data']['total_pages']}")
    print(f"  知识密度: {dashboard['brain_data']['knowledge_density']}")
    print(f"  竞争优势: {dashboard['competitive_advantage']}")

    print("\n[复利效应] 每次学习都让下一次更快更准！")


if __name__ == "__main__":
    main()
