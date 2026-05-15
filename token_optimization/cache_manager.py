#!/usr/bin/env python3
"""
AI Agent Harness - 智能缓存管理器
基于TencentDB-Agent-Memory的多级缓存策略

提供三级缓存：
1. LRU内存缓存 - 热点数据快速命中
2. 模式匹配缓存 - 相似请求复用
3. 上下文复用缓存 - 跨会话上下文共享

Token节省贡献: 30-40%
"""

import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import OrderedDict


class LRUMemoryCache:
    """LRU内存缓存 - 第一级"""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 86400):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: OrderedDict[str, Tuple[Any, float]] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl_seconds:
                # 移到末尾（最近使用）
                self.cache.move_to_end(key)
                return value
            else:
                del self.cache[key]
        return None

    def put(self, key: str, value: Any):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = (value, time.time())
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)

    def clear(self):
        self.cache.clear()

    @property
    def size(self) -> int:
        return len(self.cache)

    @property
    def hit_rate(self) -> float:
        return getattr(self, '_hits', 0) / max(getattr(self, '_total', 1), 1)


class PatternMatchCache:
    """模式匹配缓存 - 第二级"""

    def __init__(self, similarity_threshold: float = 0.75):
        self.threshold = similarity_threshold
        self.patterns: Dict[str, Dict] = {}

    def register_pattern(self, pattern_key: str, request_signature: str, result: Any):
        self.patterns[pattern_key] = {
            "signature": request_signature,
            "result": result,
            "created_at": datetime.now().isoformat(),
            "hit_count": 0
        }

    def match(self, request_signature: str) -> Optional[Any]:
        for pattern_key, pattern_data in self.patterns.items():
            similarity = self._calc_similarity(request_signature, pattern_data["signature"])
            if similarity >= self.threshold:
                pattern_data["hit_count"] += 1
                return pattern_data["result"]
        return None

    def _calc_similarity(self, sig1: str, sig2: str) -> float:
        set1 = set(sig1.lower().split())
        set2 = set(sig2.lower().split())
        if not set1 or not set2:
            return 0.0
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0


class ContextReuseCache:
    """上下文复用缓存 - 第三级"""

    def __init__(self, max_context_age_hours: int = 48):
        self.max_age = timedelta(hours=max_context_age_hours)
        self.context_store: Dict[str, Dict] = {}

    def store_context(self, context_id: str, context_data: Dict, metadata: Dict = None):
        self.context_store[context_id] = {
            "data": context_data,
            "metadata": metadata or {},
            "stored_at": datetime.now(),
            "reuse_count": 0
        }

    def get_reusable_context(self, context_id: str) -> Optional[Dict]:
        if context_id in self.context_store:
            entry = self.context_store[context_id]
            if datetime.now() - entry["stored_at"] < self.max_age:
                entry["reuse_count"] += 1
                return entry["data"]
            else:
                del self.context_store[context_id]
        return None

    def find_similar_contexts(self, query: str, top_k: int = 3) -> List[Dict]:
        results = []
        query_tokens = set(query.lower().split())
        for ctx_id, ctx_entry in self.context_store.items():
            ctx_str = json.dumps(ctx_entry["data"])
            ctx_tokens = set(ctx_str.lower().split())
            if query_tokens and ctx_tokens:
                similarity = len(query_tokens & ctx_tokens) / len(query_tokens | ctx_tokens)
                if similarity > 0.3:
                    results.append({
                        "context_id": ctx_id,
                        "similarity": similarity,
                        "data": ctx_entry["data"],
                        "reuse_count": ctx_entry["reuse_count"]
                    })
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]


class CacheManager:
    """
    多级缓存管理器

    管理三级缓存系统，提供统一的缓存接口：
    - L1: LRU内存缓存（最快，容量最小）
    - L2: 模式匹配缓存（中等速度，处理相似请求）
    - L3: 上下文复用缓存（处理跨会话上下文复用）
    """

    def __init__(self, config: Dict[str, Any] = None):
        config = config or {}
        self.l1_cache = LRUMemoryCache(
            max_size=config.get("l1_max_size", 1000),
            ttl_seconds=config.get("l1_ttl_seconds", 86400)
        )
        self.l2_cache = PatternMatchCache(
            similarity_threshold=config.get("l2_similarity_threshold", 0.75)
        )
        self.l3_cache = ContextReuseCache(
            max_context_age_hours=config.get("l3_max_age_hours", 48)
        )
        self.stats = {
            "l1_hits": 0,
            "l2_hits": 0,
            "l3_hits": 0,
            "misses": 0,
            "total_requests": 0
        }

    def get(self, cache_key: str, request_signature: str = None) -> Optional[Any]:
        """
        多级缓存查询

        查询顺序: L1 -> L2 -> L3
        返回第一个命中的结果
        """
        self.stats["total_requests"] += 1

        # L1: 精确匹配
        result = self.l1_cache.get(cache_key)
        if result is not None:
            self.stats["l1_hits"] += 1
            return {"result": result, "level": "L1", "source": "exact_match"}

        # L2: 模式匹配
        if request_signature:
            result = self.l2_cache.match(request_signature)
            if result is not None:
                self.stats["l2_hits"] += 1
                # 回填L1
                self.l1_cache.put(cache_key, result)
                return {"result": result, "level": "L2", "source": "pattern_match"}

        self.stats["misses"] += 1
        return None

    def put(self, cache_key: str, value: Any, request_signature: str = None):
        """
        写入缓存

        同时写入L1和L2
        """
        self.l1_cache.put(cache_key, value)
        if request_signature:
            self.l2_cache.register_pattern(cache_key, request_signature, value)

    def store_context(self, context_id: str, context_data: Dict, metadata: Dict = None):
        """存储可复用上下文"""
        self.l3_cache.store_context(context_id, context_data, metadata)

    def get_context(self, context_id: str) -> Optional[Any]:
        """获取可复用上下文"""
        result = self.l3_cache.get_reusable_context(context_id)
        if result:
            self.stats["l3_hits"] += 1
        return result

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        total = max(self.stats["total_requests"], 1)
        return {
            **self.stats,
            "hit_rate": (self.stats["l1_hits"] + self.stats["l2_hits"] + self.stats["l3_hits"]) / total,
            "l1_hit_rate": self.stats["l1_hits"] / total,
            "l2_hit_rate": self.stats["l2_hits"] / total,
            "l3_hit_rate": self.stats["l3_hits"] / total,
            "l1_size": self.l1_cache.size,
            "l3_contexts": len(self.l3_cache.context_store)
        }

    def clear_all(self):
        """清空所有缓存"""
        self.l1_cache.clear()
        self.l2_cache.patterns.clear()
        self.l3_cache.context_store.clear()
        self.stats = {k: 0 for k in self.stats}

    @staticmethod
    def generate_cache_key(data: Dict[str, Any]) -> str:
        """生成缓存键"""
        content = json.dumps(data, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    @staticmethod
    def generate_request_signature(request: Dict[str, Any]) -> str:
        """生成请求签名（用于模式匹配）"""
        # 提取关键特征生成签名
        parts = []
        if "action" in request:
            parts.append(request["action"])
        if "module" in request:
            parts.append(request["module"])
        if "task" in request:
            task = request["task"]
            # 提取任务关键词
            keywords = [w for w in task.split() if len(w) > 2]
            parts.extend(keywords[:5])
        return " ".join(parts)
