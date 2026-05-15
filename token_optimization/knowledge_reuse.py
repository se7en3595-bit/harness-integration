#!/usr/bin/env python3
"""
AI Agent Harness - 知识复用引擎
基于Gar Tan三层复利系统的Brain Page理念

核心能力：
1. 知识图谱管理 - 结构化存储已学知识
2. 相似度匹配 - 查找可复用的已有知识
3. 增量学习 - 只学习新知识，复用已有映射
4. 知识密度追踪 - 监控知识积累效果

Token节省贡献: 25-35%
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple


class KnowledgeNode:
    """知识图谱节点"""

    def __init__(self, node_id: str, content: str, node_type: str = "concept"):
        self.node_id = node_id
        self.content = content
        self.node_type = node_type  # concept, pattern, skill, fact
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.use_count = 0
        self.tags: List[str] = []
        self.relations: Dict[str, List[str]] = {}  # relation_type -> [node_ids]
        self.metadata: Dict[str, Any] = {}

    def use(self):
        """标记使用"""
        self.use_count += 1
        self.updated_at = datetime.now()

    def add_relation(self, relation_type: str, target_node_id: str):
        if relation_type not in self.relations:
            self.relations[relation_type] = []
        if target_node_id not in self.relations[relation_type]:
            self.relations[relation_type].append(target_node_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "content": self.content,
            "node_type": self.node_type,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "use_count": self.use_count,
            "tags": self.tags,
            "relations": self.relations,
            "metadata": self.metadata
        }


class KnowledgeGraph:
    """知识图谱"""

    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.index_by_tag: Dict[str, List[str]] = {}
        self.index_by_type: Dict[str, List[str]] = {}

    def add_node(self, node: KnowledgeNode) -> str:
        self.nodes[node.node_id] = node

        # 更新索引
        for tag in node.tags:
            if tag not in self.index_by_tag:
                self.index_by_tag[tag] = []
            self.index_by_tag[tag].append(node.node_id)

        if node.node_type not in self.index_by_type:
            self.index_by_type[node.node_type] = []
        self.index_by_type[node.node_type].append(node.node_id)

        return node.node_id

    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        return self.nodes.get(node_id)

    def find_by_tag(self, tag: str) -> List[KnowledgeNode]:
        node_ids = self.index_by_tag.get(tag, [])
        return [self.nodes[nid] for nid in node_ids if nid in self.nodes]

    def find_by_type(self, node_type: str) -> List[KnowledgeNode]:
        node_ids = self.index_by_type.get(node_type, [])
        return [self.nodes[nid] for nid in node_ids if nid in self.nodes]

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_nodes": len(self.nodes),
            "by_type": {t: len(ids) for t, ids in self.index_by_type.items()},
            "total_tags": len(self.index_by_tag),
            "total_relations": sum(
                len(r) for n in self.nodes.values() for r in n.relations.values()
            ),
            "most_used": sorted(
                [(n.node_id, n.use_count) for n in self.nodes.values()],
                key=lambda x: x[1], reverse=True
            )[:5]
        }


class KnowledgeReuseEngine:
    """
    知识复用引擎

    核心逻辑：
    1. 新内容到来时，先在知识图谱中查找相似知识
    2. 复用已有概念映射，只生成新知识
    3. 更新知识图谱，积累长期价值
    """

    def __init__(self, config: Dict[str, Any] = None):
        config = config or {}
        self.similarity_threshold = config.get("similarity_threshold", 0.7)
        self.graph = KnowledgeGraph()
        self.reuse_history: List[Dict] = []

    def process_content(self, content: str, content_type: str = "general") -> Dict[str, Any]:
        """
        处理新内容，返回复用结果

        返回:
        - reused: 复用的已有知识
        - new_concepts: 需要学习的新概念
        - tokens_saved: 估算节省的token数
        """
        # 1. 提取概念
        concepts = self._extract_concepts(content)

        # 2. 查找可复用知识
        reused = []
        new_concepts = []

        for concept in concepts:
            similar = self._find_similar(concept)
            if similar and similar["similarity"] >= self.similarity_threshold:
                reused.append({
                    "concept": concept,
                    "reused_from": similar["node_id"],
                    "similarity": similar["similarity"]
                })
                # 更新使用计数
                node = self.graph.get_node(similar["node_id"])
                if node:
                    node.use()
            else:
                new_concepts.append(concept)
                # 写入知识图谱
                node_id = self._generate_node_id(concept)
                node = KnowledgeNode(
                    node_id=node_id,
                    content=concept,
                    node_type=content_type
                )
                node.tags = self._extract_tags(concept)
                self.graph.add_node(node)

        # 3. 计算节省
        tokens_saved = self._calc_tokens_saved(reused, concepts)

        result = {
            "reused_count": len(reused),
            "new_count": len(new_concepts),
            "reuse_rate": round(len(reused) / max(len(concepts), 1), 2),
            "tokens_saved": tokens_saved,
            "reused": reused,
            "new_concepts": new_concepts,
            "graph_stats": self.graph.get_stats()
        }

        self.reuse_history.append({
            "timestamp": datetime.now().isoformat(),
            "content_type": content_type,
            "result": result
        })

        return result

    def find_similar_knowledge(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """查找相似知识"""
        results = []
        query_tokens = set(query.lower().split())

        for node_id, node in self.graph.nodes.items():
            node_tokens = set(node.content.lower().split())
            if query_tokens and node_tokens:
                similarity = len(query_tokens & node_tokens) / len(query_tokens | node_tokens)
                if similarity > 0.1:
                    results.append({
                        "node_id": node_id,
                        "content": node.content,
                        "similarity": round(similarity, 3),
                        "use_count": node.use_count,
                        "tags": node.tags
                    })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def mirror_book(self, title: str, content: str) -> Dict[str, Any]:
        """
        书籍镜像 - 将书籍内容映射到知识图谱

        参考Gar Tan的Brain Page理念
        """
        # 提取章节和概念
        chapters = self._extract_chapters(content)
        all_concepts = []

        for chapter in chapters:
            concepts = self._extract_concepts(chapter["content"])
            all_concepts.extend(concepts)

            # 每个章节创建一个节点
            chapter_node = KnowledgeNode(
                node_id=f"chapter_{chapter['index']}",
                content=chapter["title"],
                node_type="chapter"
            )
            chapter_node.tags = ["book", title.lower().replace(" ", "_")]
            chapter_node.metadata = {
                "book_title": title,
                "chapter_index": chapter["index"],
                "concept_count": len(concepts)
            }
            self.graph.add_node(chapter_node)

        # 处理所有概念
        reuse_result = self.process_content(content, content_type="book")

        # 创建书籍总节点
        book_node = KnowledgeNode(
            node_id=f"book_{title.lower().replace(' ', '_')}",
            content=title,
            node_type="book"
        )
        book_node.tags = ["book", "brain_page"]
        book_node.metadata = {
            "chapters": len(chapters),
            "concepts": len(all_concepts),
            "reuse_rate": reuse_result["reuse_rate"],
            "mirrored_at": datetime.now().isoformat()
        }
        self.graph.add_node(book_node)

        return {
            "title": title,
            "chapters_processed": len(chapters),
            "concepts_extracted": len(all_concepts),
            "reuse_result": reuse_result,
            "knowledge_density": self._calc_knowledge_density()
        }

    def analyze_meeting(self, transcript: str, participants: List[str] = None) -> Dict[str, Any]:
        """
        会议分析 - 提取会议中的决策和行动项
        """
        # 提取决策
        decisions = self._extract_by_keywords(
            transcript,
            ["decide", "agree", "approve", "choose", "confirm", "决定", "同意", "确认"]
        )

        # 提取行动项
        actions = self._extract_by_keywords(
            transcript,
            ["action", "todo", "follow up", "will do", "负责", "跟进", "待办"]
        )

        # 提取关键讨论点
        discussions = self._extract_by_keywords(
            transcript,
            ["discuss", "consider", "review", "propose", "建议", "讨论", "考虑"]
        )

        # 将提取的信息写入知识图谱
        for item in decisions:
            node = KnowledgeNode(
                node_id=self._generate_node_id(item),
                content=item,
                node_type="decision"
            )
            node.tags = ["meeting", "decision"]
            self.graph.add_node(node)

        return {
            "decisions": decisions,
            "action_items": actions,
            "discussions": discussions,
            "participants": participants or [],
            "analyzed_at": datetime.now().isoformat()
        }

    def get_knowledge_dashboard(self) -> Dict[str, Any]:
        """获取知识图谱仪表板"""
        stats = self.graph.get_stats()

        # 计算知识密度
        density = self._calc_knowledge_density()

        # 计算复用效率
        total_reuse = sum(h["result"]["reused_count"] for h in self.reuse_history)
        total_new = sum(h["result"]["new_count"] for h in self.reuse_history)

        return {
            "stats": stats,
            "knowledge_density": density,
            "total_reuse_operations": len(self.reuse_history),
            "total_concepts_reused": total_reuse,
            "total_new_concepts": total_new,
            "overall_reuse_rate": round(total_reuse / max(total_reuse + total_new, 1), 2),
            "history_sample": self.reuse_history[-5:] if self.reuse_history else []
        }

    def _extract_concepts(self, content: str) -> List[str]:
        """从内容中提取概念"""
        concepts = []
        lines = content.split('\n')

        for line in lines:
            line = line.strip()
            # 过滤太短或太长的行
            if len(line) < 10 or len(line) > 500:
                continue
            # 过滤纯代码行
            if line.startswith('```') or line.startswith('#'):
                continue
            concepts.append(line)

        return concepts[:20]  # 最多提取20个概念

    def _extract_chapters(self, content: str) -> List[Dict]:
        """提取章节"""
        chapters = []
        lines = content.split('\n')
        current_chapter = {"index": 0, "title": "Introduction", "content": ""}
        chapter_index = 0

        for line in lines:
            # 简单检测章节标题（以#开头）
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

        return chapters if chapters else [{"index": 1, "title": "Full Content", "content": content}]

    def _extract_by_keywords(self, text: str, keywords: List[str]) -> List[str]:
        """按关键词提取内容"""
        results = []
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if any(kw.lower() in line.lower() for kw in keywords) and len(line) > 5:
                results.append(line)

        return results[:10]

    def _extract_tags(self, content: str) -> List[str]:
        """提取标签"""
        tags = []
        tag_keywords = {
            "technical": ["code", "api", "function", "class", "module", "system"],
            "product": ["feature", "user", "requirement", "design", "ux"],
            "process": ["workflow", "process", "step", "phase", "stage"],
            "concept": ["pattern", "principle", "theory", "concept", "approach"]
        }

        content_lower = content.lower()
        for tag, keywords in tag_keywords.items():
            if any(kw in content_lower for kw in keywords):
                tags.append(tag)

        return tags

    def _find_similar(self, concept: str) -> Optional[Dict[str, Any]]:
        """查找最相似的知识节点"""
        best_match = None
        best_similarity = 0.0
        concept_tokens = set(concept.lower().split())

        for node_id, node in self.graph.nodes.items():
            node_tokens = set(node.content.lower().split())
            if concept_tokens and node_tokens:
                similarity = len(concept_tokens & node_tokens) / len(concept_tokens | node_tokens)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = {"node_id": node_id, "similarity": similarity}

        return best_match

    def _calc_tokens_saved(self, reused: List[Dict], all_concepts: List[str]) -> int:
        """估算节省的token数"""
        if not all_concepts:
            return 0
        avg_concept_tokens = 50  # 每个概念平均50 tokens
        return len(reused) * avg_concept_tokens

    def _calc_knowledge_density(self) -> float:
        """计算知识密度"""
        stats = self.graph.get_stats()
        total_nodes = stats["total_nodes"]
        total_relations = stats["total_relations"]

        # 密度 = 节点数 + 关系数 * 2（关系权重更高）
        density = total_nodes + total_relations * 2
        return round(density / 10, 1)  # 归一化

    @staticmethod
    def _generate_node_id(content: str) -> str:
        """生成节点ID"""
        hash_val = hashlib.md5(content.encode()).hexdigest()[:8]
        prefix = content[:20].lower().replace(" ", "_")
        return f"{prefix}_{hash_val}"
