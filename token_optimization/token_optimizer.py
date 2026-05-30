#!/usr/bin/env python3
"""
AI Agent Harness Token Optimization Module
基于TencentDB-Agent-Memory架构的token节省方案
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import asyncio

class TokenOptimizer:
    """
    Token优化引擎核心类
    提供多级缓存、上下文压缩、知识复用等功能
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._default_config()
        self.cache = TokenCache(self.config)
        self.compressor = ContextCompressor(self.config)
        self.reuse_engine = KnowledgeReuseEngine(self.config)
        self.budget_manager = TokenBudgetManager(self.config)

    def _default_config(self) -> Dict[str, Any]:
        """默认配置"""
        return {
            "max_cache_size": 1000,
            "cache_ttl_hours": 24,
            "compression_ratio": 0.3,
            "budget_limit_per_call": 10000,
            "enable_knowledge_reuse": True,
            "enable_context_compression": True
        }

    async def optimize_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        优化请求处理流程
        """
        # 1. 检查缓存
        cached_result = await self.cache.get_cached_result(request_data)
        if cached_result:
            return cached_result

        # 2. 预算检查
        budget_check = self.budget_manager.check_budget(request_data)
        if not budget_check["allowed"]:
            return budget_check

        # 3. 压缩输入数据
        compressed_input = self.compressor.compress_context(
            request_data.get("context", [])
        )

        # 4. 优化prompt
        optimized_prompt = self._optimize_prompt(
            request_data.get("prompt", ""),
            compressed_input
        )

        # 5. 执行核心逻辑（模拟）
        result = await self._execute_core_logic(optimized_prompt, compressed_input)

        # 6. 压缩输出
        compressed_result = self.compressor.compress_output(result)

        # 7. 缓存结果
        await self.cache.cache_result(request_data, compressed_result)

        return {
            "result": compressed_result,
            "tokens_saved": self._calculate_tokens_saved(request_data, result),
            "optimization_applied": True
        }

    def _optimize_prompt(self, original_prompt: str, context: List[Dict]) -> str:
        """优化prompt长度和复杂度"""
        # 1. 模板化prompt
        if len(original_prompt) > 8000:
            return self._generate_template_prompt(context)

        # 2. 移除冗余
        cleaned_prompt = self._remove_redundant_parts(original_prompt)

        # 3. 关键信息提取
        key_instruction = extract_key_instruction(cleaned_prompt)

        return f"{key_instruction}\n\nContext: {json.dumps(context[:3], indent=2)}"

    async def _execute_core_logic(self, prompt: str, context: List[Dict]) -> Dict[str, Any]:
        """
        处理优化后的 prompt 和 context，返回结构化结果。

        这里不调用外部 AI 模型——TokenOptimizer 的职责是
        压缩/缓存/预算管理，实际 AI 调用由上层调用方负责。
        """
        return {
            "optimized_prompt": prompt,
            "compressed_context_items": len(context),
            "metadata": {
                "prompt_length": len(prompt),
                "context_items": len(context),
                "processed_at": datetime.now().isoformat()
            }
        }

    def _calculate_tokens_saved(self, original_request: Dict, optimized_result: Dict) -> int:
        """
        基于实际字符数估算节省的 token 数。

        原始大小 = original_request 的 JSON 字符数
        优化后大小 = optimized_result 中 optimized_prompt 的字符数
                    + compressed_context_items 数量（每项按 50 字符估算）
        差值转换为 token（1 字符 ≈ 0.4 token，中英混合取保守值）
        """
        original_chars = len(json.dumps(original_request, ensure_ascii=False))

        optimized_prompt_chars = len(optimized_result.get("optimized_prompt", ""))
        context_items = optimized_result.get("compressed_context_items", 0)
        optimized_chars = optimized_prompt_chars + context_items * 50

        chars_saved = max(original_chars - optimized_chars, 0)
        # 1 字符 ≈ 0.4 token（保守估算，避免虚报）
        return int(chars_saved * 0.4)


class TokenCache:
    """多级缓存系统"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.memory_cache = {}
        self.pattern_cache = {}
        self.ttl_tracker = {}

    async def get_cached_result(self, request_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """获取缓存结果"""
        cache_key = self._generate_cache_key(request_data)

        # 检查内存缓存
        if cache_key in self.memory_cache:
            result, timestamp = self.memory_cache[cache_key]

            # 检查TTL
            if self._is_cache_valid(timestamp):
                return result
            else:
                del self.memory_cache[cache_key]

        # 检查模式缓存
        pattern_match = self._find_pattern_match(request_data)
        if pattern_match:
            return pattern_match

        return None

    async def cache_result(self, request_data: Dict[str, Any], result: Dict[str, Any]):
        """缓存结果"""
        cache_key = self._generate_cache_key(request_data)

        # 限制缓存大小
        if len(self.memory_cache) >= self.config["max_cache_size"]:
            self._evict_oldest_entry()

        self.memory_cache[cache_key] = (result, datetime.now())
        self.ttl_tracker[cache_key] = datetime.now()

    def _generate_cache_key(self, data: Dict[str, Any]) -> str:
        """生成缓存键"""
        # 使用哈希避免敏感信息泄露
        content = json.dumps(data, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()

    def _is_cache_valid(self, timestamp: datetime) -> bool:
        """检查缓存是否有效"""
        ttl = timedelta(hours=self.config["cache_ttl_hours"])
        return datetime.now() - timestamp < ttl

    def _find_pattern_match(self, request_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """查找模式匹配"""
        request_text = json.dumps(request_data).lower()

        for pattern, cached_result in self.pattern_cache.items():
            if pattern in request_text:
                return cached_result

        return None

    def _evict_oldest_entry(self):
        """淘汰最老的缓存项"""
        if not self.memory_cache:
            return

        oldest_key = min(
            self.memory_cache.keys(),
            key=lambda k: self.memory_cache[k][1]
        )
        del self.memory_cache[oldest_key]


class ContextCompressor:
    """上下文压缩器"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def compress_context(self, context_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """压缩上下文"""
        if not context_list:
            return []

        # 1. 移除调试噪音
        clean_context = self._remove_debug_noise(context_list)

        # 2. 保留关键状态
        essential_state = self._extract_essential_state(clean_context)

        # 3. 编码压缩
        return self._encode_compressed(essential_state)

    def compress_output(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """压缩输出"""
        # 1. 结构化摘要
        summary = self._generate_summary(output)

        # 2. 关键信息提取
        key_points = extract_key_points(output)

        # 3. 压缩编码
        compressed = {
            "summary": summary,
            "details": key_points,
            "metadata": {
                "compressed_at": datetime.now().isoformat(),
                "compression_ratio": len(str(summary)) / len(str(output))
            }
        }

        return compressed

    def _remove_debug_noise(self, context: List[Dict]) -> List[Dict]:
        """移除调试噪音"""
        clean = []
        for item in context:
            # 移除调试日志、临时变量等
            if not any(keyword in str(item).lower()
                      for keyword in ["debug", "temp", "tmp", "log"]):
                clean.append(item)
        return clean

    def _extract_essential_state(self, context: List[Dict]) -> Dict[str, Any]:
        """提取关键状态"""
        state = {
            "entities": [],
            "actions": [],
            "decisions": [],
            "errors": []
        }

        for item in context:
            content = str(item).lower()

            # 提取实体
            if any(entity_type in content
                  for entity_type in ["user", "task", "project"]):
                state["entities"].append(item)

            # 提取动作
            elif any(action in content
                    for action in ["create", "update", "delete", "execute"]):
                state["actions"].append(item)

            # 提取决策
            elif any(decision in content
                    for decision in ["choose", "select", "decide"]):
                state["decisions"].append(item)

            # 提取错误
            elif any(error in content
                    for error in ["error", "fail", "exception"]):
                state["errors"].append(item)

        return state

    def _encode_compressed(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """编码压缩数据"""
        encoded = []

        # 压缩实体
        if data["entities"]:
            encoded.append({
                "type": "entities",
                "count": len(data["entities"]),
                "hash": hashlib.md5(str(data["entities"][:3]).encode()).hexdigest()
            })

        # 压缩动作
        if data["actions"]:
            encoded.append({
                "type": "actions",
                "count": len(data["actions"]),
                "primary": data["actions"][0] if data["actions"] else None
            })

        return encoded

    def _generate_summary(self, output: Dict[str, Any]) -> str:
        """生成摘要"""
        # 提取关键信息生成摘要
        if "response" in output:
            response = output["response"]
            if len(response) > 200:
                return response[:200] + "..."
            return response
        return str(output)[:200]


class KnowledgeReuseEngine:
    """知识复用引擎"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.knowledge_graph = {}
        self.concept_mappings = {}

    def find_similar_knowledge(self, new_content: str) -> List[Dict[str, Any]]:
        """查找相似已有知识"""
        similar_items = []

        # 基于语义相似度查找
        for concept_id, concept_data in self.concept_mappings.items():
            similarity = self._calculate_similarity(new_content, concept_data["content"])
            if similarity > 0.7:  # 70%相似度阈值
                similar_items.append({
                    "concept_id": concept_id,
                    "similarity": similarity,
                    "reused_data": concept_data
                })

        return sorted(similar_items, key=lambda x: x["similarity"], reverse=True)

    def reuse_existing_mappings(self, similar_knowledge: List[Dict]) -> List[Dict[str, Any]]:
        """重用现有映射"""
        reused_mappings = []

        for item in similar_knowledge:
            # 重用概念映射
            reused_mappings.append({
                "type": "concept_mapping",
                "source": item["concept_id"],
                "similarity": item["similarity"],
                "data": item["reused_data"]["mapping"]
            })

            # 更新知识图谱
            self._update_knowledge_graph(item)

        return reused_mappings

    def generate_new_concepts(self, content: str, reused_mappings: List[Dict]) -> List[Dict[str, Any]]:
        """生成新知识"""
        # 从内容中提取未被重用的概念
        all_concepts = self._extract_concepts(content)
        used_concept_ids = [m["source"] for m in reused_mappings if "source" in m]

        new_concepts = [
            concept for concept in all_concepts
            if concept["id"] not in used_concept_ids
        ]

        return new_concepts

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度"""
        # 简化的相似度计算
        set1 = set(text1.lower().split())
        set2 = set(text2.lower().split())

        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        return intersection / union if union > 0 else 0.0

    def _update_knowledge_graph(self, item: Dict[str, Any]):
        """更新知识图谱"""
        concept_id = item["concept_id"]
        if concept_id not in self.knowledge_graph:
            self.knowledge_graph[concept_id] = {
                "created_at": datetime.now().isoformat(),
                "usage_count": 0,
                "last_used": datetime.now().isoformat()
            }

        self.knowledge_graph[concept_id]["usage_count"] += 1
        self.knowledge_graph[concept_id]["last_used"] = datetime.now().isoformat()

    def _extract_concepts(self, content: str) -> List[Dict[str, Any]]:
        """从内容中提取概念"""
        concepts = []

        # 简单的概念提取逻辑
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if len(line.strip()) > 10 and not line.startswith('#'):
                concept_id = f"concept_{len(concepts) + 1}"
                concepts.append({
                    "id": concept_id,
                    "content": line.strip(),
                    "position": i,
                    "length": len(line)
                })

        return concepts


class TokenBudgetManager:
    """Token预算管理器"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.usage_history = {}

    def check_budget(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """检查预算"""
        # 估算本次请求的token需求
        estimated_tokens = self._estimate_token_usage(request_data)

        # 检查预算限制
        if estimated_tokens > self.config["budget_limit_per_call"]:
            return {
                "allowed": False,
                "reason": "exceeds_budget",
                "required_tokens": estimated_tokens,
                "max_allowed": self.config["budget_limit_per_call"],
                "suggestion": "break_into_smaller_tasks"
            }

        return {"allowed": True, "estimated_tokens": estimated_tokens}

    def _estimate_token_usage(self, request_data: Dict[str, Any]) -> int:
        """估算token使用量"""
        total_size = 0

        # 计算prompt大小
        if "prompt" in request_data:
            total_size += len(str(request_data["prompt"]))

        # 计算context大小
        if "context" in request_data:
            total_size += len(json.dumps(request_data["context"]))

        # 计算额外数据大小
        if "additional_data" in request_data:
            total_size += len(json.dumps(request_data["additional_data"]))

        # 转换为大致的token数（1字符≈1.3 tokens）
        return int(total_size * 1.3)


# 辅助函数
def extract_key_instruction(prompt: str) -> str:
    """提取关键指令"""
    # 简化版本：提取第一行作为关键指令
    lines = prompt.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('```'):
            return line
    return prompt[:200]


def extract_key_points(data: Dict[str, Any]) -> List[str]:
    """提取关键点"""
    key_points = []

    # 从常见字段中提取关键信息
    for field in ["result", "response", "output", "answer"]:
        if field in data and isinstance(data[field], str):
            if len(data[field]) > 50:
                key_points.append(f"{field}: {data[field][:100]}...")
            else:
                key_points.append(f"{field}: {data[field]}")

    return key_points


# 全局优化器实例
global_optimizer = TokenOptimizer()

async def optimize_request_sync(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """同步接口函数"""
    return await global_optimizer.optimize_request(request_data)


if __name__ == "__main__":
    # 示例使用
    async def main():
        optimizer = TokenOptimizer()

        test_request = {
            "prompt": "请帮我实现一个用户登录功能，包括验证、权限管理等",
            "context": [
                {"type": "previous_task", "description": "用户认证系统设计"},
                {"type": "requirements", "description": "需要支持JWT令牌"}
            ]
        }

        result = await optimizer.optimize_request(test_request)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    import asyncio
    asyncio.run(main())